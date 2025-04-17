#!/usr/bin/zsh
#SBATCH --beeond
#SBATCH --exclusive
#SBATCH --job-name=mpi_sim
#SBATCH --time=01:59:00
#SBATCH --output=recorder_mpi_sim_%j.out
#SBATCH --ntasks=2
#SBATCH --nodes=1

#SBATCH --account=thes1876

# Load required libs
ml purge
ml load iimpi
ml load HDF5

export RECORDER_POSIX_TRACING=1
export RECORDER_MPIIO_TRACING=1
export RECORDER_MPI_TRACING=1
export RECORDER_HDF5_TRACING=1
export RECORDER_TRACES_DIR=/hpcwork/ph077533/sim_results/recorder

cp $HPCWORK/claix-hpc-io/simulation/mpi_io_sim $BEEOND
LD_PRELOAD=$HPCWORK/recorder-claix-2023/install/lib/librecorder.so $MPIEXEC $BEEOND/mpi_io_sim


