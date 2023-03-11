#include <stdio.h>
#include <time.h>

int main() {
    struct timespec start_time, end_time;
    double elapsed_time;

    clock_gettime(CLOCK_MONOTONIC, &start_time);

    // Do some work here

    clock_gettime(CLOCK_MONOTONIC, &end_time);

    elapsed_time = (end_time.tv_sec - start_time.tv_sec) +
                   (double)(end_time.tv_nsec - start_time.tv_nsec) / 1000000000.0;

    printf("Elapsed time: %f seconds\n", elapsed_time);
    return 0;
}
