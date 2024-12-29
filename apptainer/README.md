# Jupyter Server on CLAIX-2023 with Apptainer

This guide provides instructions to set up and run a Jupyter Server on CLAIX-2023 using Apptainer, enabling work with files on the cluster file system.

## Components
- **`requirements.txt`**: Lists the necessary packages to be installed in the environment for running Jupyter.
- **`data_analysis_apptainer.def`**: Definition file for building the container.
    - The `\workspace` directory will be created during the container execution, and the Jupyter server will run in this directory.

## Build and Run the Container
1. **Build the Container**: A `.sif` file will be created after a successful build.
    ```sh
    apptainer build jupyter_container.sif data_analysis_apptainer.def
    ```

2. **Run the Container**: Use the `.sif` file to run the container.
    ```sh
    apptainer run jupyter_container.sif
    ```

3. **Mount Data**: To work with data on the cluster filesystem, mount the necessary directories (e.g., `$HPCWORK` or `$WORK`) to the `\workspace` directory for easy access.
    ```sh
    apptainer run --bind $HPCWORK:/workspace jupyter_container.sif
    ```