#include <stdio.h>
#include <gpiod.h>
#include <pthread.h>
#include <time.h>

int counter1 = 0, counter2 = 0;

void* counter_1(void* arg) {

    struct gpiod_chip *chip;
    struct gpiod_line *line;
    struct gpiod_line_event event;
    int ret;

    struct timespec start_time, end_time;
    double elapsed_time_1;

    // Open the GPIO chip device
    chip = gpiod_chip_open_by_number(0);
    if (!chip) {
        printf("Failed to open GPIO chip\n");
    }

    // Request the GPIO line for pin 194
    line = gpiod_chip_get_line(chip, 194);
    if (!line) {
        printf("Failed to get GPIO line\n");
    }

    // Configure the line for input and rising-edge interrupt events
    ret = gpiod_line_request_rising_edge_events(line, "my_program");
    if (ret < 0) {
        printf("Failed to request GPIO interrupt events\n");
    }

    // if pin 15(linux194)= up counter1++
    while(counter1<15) {
        counter1++;

        clock_gettime(CLOCK_MONOTONIC, &start_time);

        ret = gpiod_line_event_wait(line, NULL);
        if (ret < 0) {
            printf("Failed to wait for GPIO events\n");
        }
        ret = gpiod_line_event_read(line, &event);
        if (ret < 0) {
            printf("Failed to read GPIO events\n");
        }

        
        clock_gettime(CLOCK_MONOTONIC, &end_time);

        elapsed_time_1 = (end_time.tv_sec - start_time.tv_sec) +
                   (double)(end_time.tv_nsec - start_time.tv_nsec) / 1000000000.0;

        printf("Elapsed time 1 : %f seconds\n", elapsed_time_1);


    }
    gpiod_line_release(line);
    gpiod_chip_close(chip);

    pthread_exit(NULL);
}

void* counter_2(void* arg) {

    struct gpiod_chip *chip;
    struct gpiod_line *line;
    struct gpiod_line_event event;
    int ret;

    struct timespec start_time, end_time;
    double elapsed_time_2;

    // Open the GPIO chip device
    chip = gpiod_chip_open_by_number(0);
    if (!chip) {
        printf("Failed to open GPIO chip\n");
    }

    // Request the GPIO line for pin 149
    line = gpiod_chip_get_line(chip, 149);
    if (!line) {
        printf("Failed to get GPIO line\n");
    }

    // Configure the line for input and rising-edge interrupt events
    ret = gpiod_line_request_rising_edge_events(line, "my_program");
    if (ret < 0) {
        printf("Failed to request GPIO interrupt events\n");
    }


    // if pin 29(linux149)= up counter1++
    while(counter2<29) {
        counter2++;

        clock_gettime(CLOCK_MONOTONIC, &start_time);

        ret = gpiod_line_event_wait(line, NULL);
        if (ret < 0) {
            printf("Failed to wait for GPIO events\n");
        }
        ret = gpiod_line_event_read(line, &event);
        if (ret < 0) {
            printf("Failed to read GPIO events\n");
        }

        
        clock_gettime(CLOCK_MONOTONIC, &end_time);

        elapsed_time_2 = (end_time.tv_sec - start_time.tv_sec) +
                   (double)(end_time.tv_nsec - start_time.tv_nsec) / 1000000000.0;

        printf("Elapsed time 2 : %f seconds\n", elapsed_time_2);
    }
    gpiod_line_release(line);
    gpiod_chip_close(chip);

    pthread_exit(NULL);
}

int main() {
    pthread_t thread_id1, thread_id2;

    pthread_create(&thread_id1, NULL, counter_1, NULL);
    pthread_create(&thread_id2, NULL, counter_2, NULL);

    pthread_join(thread_id1, NULL);
    pthread_join(thread_id2, NULL);

    printf("Counter1 = %d, Counter2 = %d\n", counter1, counter2);

    return 0;
}