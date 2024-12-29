import os
import argparse
import tempfile
import itertools
import subprocess
from jinja2 import Template

# Define template file mapping
TEMPLATE_FILES = "./templates/tracing_template.j2"

MODES = ["darshan", "recorder", "scorep"]

# Configurable paths
BINARY_PATH = "$HPCWORK/NPB-claix-2023/NPB3.4-MPI/bin"
LIBRARY_PATHS = {
    "darshan": "$HPCWORK/darshan_runtime-claix_2023/lib/libdarshan.so",
    "recorder": "$HPCWORK/recorder-claix-2023/install/lib/librecorder.so",
    "scorep": None
}
OUTPUT_PATH = {
    "darshan": "$HPCWORK/darshan-results",
    "recorder": "$HPCWORK/recorder-results",
    "scorep": "$HPCWORK/scorep-results"
}

LOG_PATH = "$HPCWORK/beeond-logs"

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
    if library_path:
        library_path = os.path.expandvars(library_path)
        if not (os.path.isfile(library_path) and os.path.islink(library_path)):
            missing_files.append(f"Library not found: {library_path}")

    if missing_files:
        print("Validation failed for the following files:")
        for missing in missing_files:
            print(f"  - {missing}")
        exit(1)

def main(mode, ntasks_list, binaries):
    """Main function to create and submit jobs."""
    # Load the appropriate template
    if mode not in MODES:
        print(f"Error: Unsupported mode '{mode}'.")
        exit(1)

    slurm_template = load_template(TEMPLATE_FILES)

    # Validate binaries and libraries
    validate_binaries_and_libraries(mode, binaries)

    # Generate combinations of ntasks and binaries
    library_path = LIBRARY_PATHS.get(mode)  # Fetch library path for substitution

    result_path = os.path.expandvars(
        OUTPUT_PATH.get(mode)
    )

    # Check if result_path exists, if not create it
    if not os.path.exists(result_path):
        os.makedirs(result_path)

    log_path = os.path.expandvars(LOG_PATH)
    
    # Check if log_path exists, if not create it
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    combinations = itertools.product(ntasks_list, binaries)
    # Submit jobs
    for ntasks, binary in combinations:
        # Render the script with ntasks, binary, and paths
        binary_path = os.path.join(
            os.path.expandvars(BINARY_PATH), binary
        )

        script_content = slurm_template.render(
            mode=mode,
            ntasks=ntasks,
            binary=binary,
            binary_path=binary_path,
            library_path=library_path,
            log_path=log_path,
            result_path=result_path,
        )

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
        help="Mode of operation: 'darshan', 'recorder', or 'scorep'"
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
