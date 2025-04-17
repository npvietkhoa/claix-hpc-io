make all
rm *.out
sbatch darshan_mpi_sim.sh
sbatch recorder_mpi_sim.sh
sbatch scorep_mpi_sim.sh
