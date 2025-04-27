# === Configuration ===
MPICC ?= mpicc
SRC    = mpi_io_sim.c
BIN    = mpi_io_sim
BIN_S  = scorep_mpi_io_sim

# === Flags ===
CFLAGS = -O2

# === Targets ===

all: $(BIN) $(BIN_S)

$(BIN): $(SRC)
	$(MPICC) $(CFLAGS) -o $@ $^

$(BIN_S): $(SRC)
	scorep --io=runtime:posix $(MPICC) $(CFLAGS) -o $@ $^

clean:
	rm -f $(BIN) $(BIN_S)
	rm -rf scorep-*

.PHONY: all clean

