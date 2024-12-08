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

