#include <stdio.h>
#include <sys/time.h>

int main() {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    unsigned long long microseconds_since_epoch =
        (unsigned long long)(tv.tv_sec) * 1000000 +
        (unsigned long long)(tv.tv_usec);
    printf("Current time: %llu microseconds since Epoch\n", microseconds_since_epoch);
    return 0;
}
