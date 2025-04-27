#!/usr/bin/zsh
#SBATCH --beeond
#SBATCH --exclusive
#SBATCH --job-name=mpi_sim
#SBATCH --time=01:59:00
#SBATCH --output=scorep_mpi_sim_%j.out
#SBATCH --ntasks=2
#SBATCH --nodes=1

#SBATCH --account=thes1876

# Load required libs
ml purge
ml load iimpi
ml load HDF5


export SCOREP_EXPERIMENT_DIRECTORY=/hpcwork/ph077533/sim_results/scorep
export SCOREP_ENABLE_TRACING=true

cp $HPCWORK/claix-hpc-io/simulation/scorep_mpi_io_sim $BEEOND

$MPIEXEC $BEEOND/scorep_mpi_io_sim

