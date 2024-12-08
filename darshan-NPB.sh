#!/usr/bin/zsh

# --- Job Parameters ---
#SBATCH --job-name=darshan-npb
#SBATCH --time=00:30:00
#SBATCH --ntasks=4           # Number of MPI tasks
#SBATCH --nodes=1            # Use one node for this job
#SBATCH --mem-per-cpu=2G     # Adjust the memory per CPU as necessary

### Beginning of executable commands
export DARSHAN_LOGPATH=.
LD_PRELOAD=$HOME/darshan/lib/libdarshan.so 

$MPIEXEC $FLAGS_MPI_BATCH $HOME/NPB3.3.1/NPB3.3-MPI/bin/bt.A.9.mpi_io_full