#!/usr/bin/zsh

# --- Job Parameters ---
#SBATCH --job-name=scorep-npb
#SBATCH --time=00:30:00
#SBATCH --ntasks=4           # Number of MPI tasks
#SBATCH --nodes=1            # Use one node for this job
#SBATCH --mem-per-cpu=2G     # Adjust the memory per CPU as necessary

### Declare the merged STDOUT/STDERR file
#SBATCH --output=output.%J.txt

### Beginning of executable commands
$MPIEXEC $FLAGS_MPI_BATCH $HOME/NPB3.3.1/NPB3.3-MPI/BT/bt-full.mpi_io_full