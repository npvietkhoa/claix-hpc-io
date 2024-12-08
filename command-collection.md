Instrument ScoreP within NPB3.3.1 NAS Benchmark
```
make bt-full \
       FLINK="scorep ${MPIFC}" \
       FLINKFLAGS="${FLAGS_DEBUG} -lm" \
       PROGRAM=bt-full \
       NPROCS=9 \
       CLASS=A \
       SUBTYPE=full
```

