#!/usr/bin/zsh

# --- Job Parameters ---
#SBATCH --job-name=recorder_mpi_profiling
#SBATCH --time=00:30:00
#SBATCH --ntasks=4           # Number of MPI tasks
#SBATCH --nodes=1            # Use one node for this job
#SBATCH --mem-per-cpu=2G     # Adjust the memory per CPU as necessary

# --- Environment Setup ---
module purge
module load iimpi
module load HDF5

LD_PRELOAD=$HOME/Recorder/install/lib/librecorder.so
export LD_PRELOAD

$MPIEXEC $HOME/Recorder/test/test_mpi