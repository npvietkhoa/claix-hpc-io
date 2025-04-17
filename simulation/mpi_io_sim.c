#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define FILENAME "mpi_io_sim.dat"
#define BUF_SIZE 1000000  // 1MB buffer
#define NUM_IO_OPS 4

int main(int argc, char **argv) {
    int rank, size;
    MPI_File fh;
    MPI_Status status;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (size != 2) {
        if (rank == 0) {
            fprintf(stderr, "This program must be run with exactly 2 ranks.\n");
        }
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    MPI_Offset offset = rank * BUF_SIZE;

    for (int i = 0; i < NUM_IO_OPS; ++i) {
        char write_buf[BUF_SIZE];
        // Fill entire buffer with pattern
        for (int j = 0; j < BUF_SIZE - 1; j++) {
            write_buf[j] = 'A' + ((rank + i) % 26);
        }
        write_buf[BUF_SIZE - 1] = '\0';

        // Write operation
        MPI_File_open(MPI_COMM_WORLD, FILENAME,
                      MPI_MODE_CREATE | MPI_MODE_WRONLY,
                      MPI_INFO_NULL, &fh);
        MPI_File_write_at(fh, offset, write_buf, BUF_SIZE, MPI_CHAR, &status);
        MPI_File_close(&fh);

        MPI_Barrier(MPI_COMM_WORLD);

        // Read operation
        char read_buf[BUF_SIZE];
        memset(read_buf, 0, BUF_SIZE);

        MPI_File_open(MPI_COMM_WORLD, FILENAME,
                      MPI_MODE_RDONLY, MPI_INFO_NULL, &fh);
        MPI_File_read_at(fh, offset, read_buf, BUF_SIZE, MPI_CHAR, &status);
        MPI_File_close(&fh);
    }

    MPI_Finalize();
    return 0;
}
