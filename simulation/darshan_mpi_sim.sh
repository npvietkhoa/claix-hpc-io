#!/usr/bin/zsh
#SBATCH --beeond
#SBATCH --exclusive
#SBATCH --job-name=mpi_sim
#SBATCH --time=01:59:00
#SBATCH --output=darshan_mpi_sim_%j.out
#SBATCH --ntasks=2
#SBATCH --nodes=1

#SBATCH --account=thes1876

# Load required libs
ml purge
ml load iimpi
ml load HDF5

export DARSHAN_LOGPATH=/hpcwork/ph077533/sim_results/darshan
export DXT_ENABLE_IO_TRACE=1

cp $HPCWORK/claix-hpc-io/simulation/mpi_io_sim $BEEOND
LD_PRELOAD=$HPCWORK/darshan_runtime-claix_2023/lib/libdarshan.so $MPIEXEC $BEEOND/mpi_io_sim


