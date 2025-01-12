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

# Generate Summary with `pydarshan`
- Ofc, `pydarshan` is needed
```
python -m darshan summary ~/path/to/log_file.darshan
```
- Batch generate for `.darshan` files in current directory
```
find . -name "*.darshan" -exec python -m darshan summary {} \;
```

# Recorder Result to OTF2 Tracing File

## Generate Chrome Trace File from Recorder Results
- Utilize `recorder2timeline` from Recorder to build Chrome Timeline (`.json` files).
- Convert Chrome Timeline to OTF2 using [`otf2_cli_chrome_trace_converter`](https://github.com/score-p/otf2_cli_chrome_trace_converter).

### 1. Building Timeline
- **Remark:** This command should be performed inside the recorder result collection directory. Otherwise, ensure the paths are correct.
```bash
for dir in */; do
    recorder2timeline "$dir"
done
```

### 2. Convert Recorder Results to OTF2 Tracings.
- Ensure required packages are installed for `chrome2otf2` (see `requirements.txt`).
- This command should be performed inside the recorder result collection directory. Otherwise, ensure the paths are correct.
- OTF2 Trace Files will be generated inside the directory where the Chrome Timeline folder is located, i.e., `$dir`.
```bash
for dir in */; do
    if [ -d "$dir/_chrome" ]; then
        python chrome2otf2.py -i "$dir/_chrome/timeline_0.json" -o "$dir"
        echo "$dir - success"
    else
        echo "$dir has no timeline"
    fi
done
```
