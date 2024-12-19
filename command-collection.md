# NPB Benchmark Build
1. create Makefile 

    `cp config/make.def.template config/make.def`

2. Set the following make variables in config/make.def:

    - `MPIF77 = mpif90` ~ `$MPIFC`
    - `FFLAGS = -O2 -g`
3. `make bt NPROCS=9 CLASS=A SUBTYPE=full`
4. This will create the executable in bin/bt.A.9.mpi_io_full

# Instrument ScoreP within NPB3.3.1 NAS Benchmark
```
make bt-full \
       FLINK="scorep ${MPIFC}" \
       FLINKFLAGS="${FLAGS_DEBUG} -lm" \
       PROGRAM=bt-full \
       NPROCS=9 \
       CLASS=A \
       SUBTYPE=full
```

# Build NPB3.4.3 with suite
```
make suite \
    SFILE=./config/suite.A.def \
    MPIFC=$MPIFC \
    MPICC=$MPICC \
```

# Build Recorder
```bash
cmake .. \
  -DCMAKE_INSTALL_PREFIX=$RECORDER_INSTALL_PATH \
  -DCMAKE_CXX_COMPILER=$MPICXX \
  -DCMAKE_PREFIX_PATH=/cvmfs/software.hpc.rwth.de/Linux/RH8/x86_64/intel/sapphirerapids/software/HDF5/1.14.0-iimpi-2022a
```
- Remarks:
    - `RECORDER_INSTALL_PATH=`pwd`/install` in Recorder directory
    - `$MPICXX` as env. Variable (dynamically assign as env in cluster)
    - `/cvmfs/software.hpc.rwth.de/Linux/RH8/x86_64/intel/sapphirerapids/software/HDF5/1.14.0-iimpi-2022a` for HDF5 libs


