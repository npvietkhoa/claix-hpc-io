import os
import argparse
import tempfile
import itertools
import subprocess
from jinja2 import Template

# Define template file mapping
TEMPLATE_FILES = {
    "darshan": "./templates/darshan_template.j2",
    "recorder": "./templates/recorder_template.j2",
    "scorep": "./templates/scorep_template.j2"
}

# Configurable paths
BINARY_PATH = "$HPCWORK/NPB3.4.3/NPB3.4-MPI/bin"
LIBRARY_PATHS = {
    "darshan": "$HPCWORK/Darshan/lib/libdarshan.so",
    "darshan": "$HPCWORK/Recorder/install/lib/librecorder.so",
    "scorep": None
}
def load_template(template_file):
    """Load the Slurm template from a file."""
    try:
        with open(template_file, 'r') as file:
            return Template(file.read())
    except FileNotFoundError:
        print(f"Error: Template file '{template_file}' not found.")
        exit(1)

def validate_binaries_and_libraries(mode, binaries):
    """Check if binaries and required libraries are available."""
    missing_files = []

    # Expand environment variable for binary path
    expanded_binary_path = os.path.expandvars(BINARY_PATH)

    # Validate binaries
    for binary in binaries:
        binary_path = os.path.join(expanded_binary_path, binary)
        if not os.path.isfile(binary_path):
            missing_files.append(f"Binary not found: {binary_path}")

    # Validate libraries (if applicable)
    library_path = LIBRARY_PATHS.get(mode)
    if library_path and not os.path.isfile(library_path):
        missing_files.append(f"Library not found: {library_path}")

    if missing_files:
        print("Validation failed for the following files:")
        for missing in missing_files:
            print(f"  - {missing}")
        exit(1)

def main(mode, ntasks_list, binaries):
    """Main function to create and submit jobs."""
    # Load the appropriate template
    if mode not in TEMPLATE_FILES:
        print(f"Error: Unsupported mode '{mode}'. Choose from {list(TEMPLATE_FILES.keys())}.")
        exit(1)

    template_file = TEMPLATE_FILES[mode]
    slurm_template = load_template(template_file)

    # Validate binaries and libraries
    validate_binaries_and_libraries(mode, binaries)

    # Generate combinations of ntasks and binaries
    library_path = LIBRARY_PATHS.get(mode)  # Fetch library path for substitution
    combinations = itertools.product(ntasks_list, binaries)

    # Submit jobs
    for ntasks, binary in combinations:
        # Render the script with ntasks, binary, and paths
        script_content = slurm_template.render(
            ntasks=ntasks,
            binary=binary,
            binary_path=BINARY_PATH,
            library_path=library_path
        )

        # Create a temporary file with delete=True
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=True) as temp_file:
            temp_file.write(script_content)
            temp_file.flush()  # Ensure content is written to disk

            # Submit the job
            try:
                subprocess.run(["sbatch", temp_file.name], check=True)
                print(f"Submitted job for ntasks={ntasks}, binary={binary}, mode={mode}")
            except subprocess.CalledProcessError as e:
                print(f"Error submitting job for ntasks={ntasks}, binary={binary}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate and submit Slurm jobs for Darshan, Recorder, or Score-P."
    )
    parser.add_argument(
        "--mode",
        type=str,
        required=True,
        help="Mode of operation: 'Darshan', 'Recorder', or 'ScoreP'"
    )
    parser.add_argument(
        "--ntasks_list",
        type=int,
        nargs='+',
        required=True,
        help="List of ntasks (e.g., 1 2 4 9 16 25)"
    )
    parser.add_argument(
        "--binaries",
        type=str,
        nargs='+',
        required=True,
        help="List of binaries (e.g., bt.A.x.mpi_io_full)"
    )

    args = parser.parse_args()

    # Call the main function with arguments
    main(args.mode, args.ntasks_list, args.binaries)
