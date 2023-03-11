#include <stdio.h>
#include <gpiod.h>
#include <time.h>

int main()
{
    struct gpiod_chip *chip;
    struct gpiod_line *line;
    struct gpiod_line_event event;
    int ret;

    struct timespec start_time, end_time;
    double elapsed_time;

    int count = 0;

    // Open the GPIO chip device
    chip = gpiod_chip_open_by_number(0);
    if (!chip) {
        printf("Failed to open GPIO chip\n");
        return 1;
    }

    // Request the GPIO line for pin 194
    line = gpiod_chip_get_line(chip, 194);
    if (!line) {
        printf("Failed to get GPIO line\n");
        return 1;
    }

    // Configure the line for input and rising-edge interrupt events
    ret = gpiod_line_request_rising_edge_events(line, "my_program");
    if (ret < 0) {
        printf("Failed to request GPIO interrupt events\n");
        return 1;
    }

    // Wait for and handle GPIO interrupt events
    
    while (1) {
        count++;

        clock_gettime(CLOCK_MONOTONIC, &start_time);

        printf("count: %i\n",count);
        
        ret = gpiod_line_event_wait(line, NULL);
        if (ret < 0) {
            printf("Failed to wait for GPIO events\n");
            return 1;
        }
        ret = gpiod_line_event_read(line, &event);
        if (ret < 0) {
            printf("Failed to read GPIO events\n");
            return 1;
        }
        printf("GPIO event received: timestamp=%lld.%09ld, event_type=%d\n",
                (long long)event.ts.tv_sec, event.ts.tv_nsec, event.event_type);
        
        clock_gettime(CLOCK_MONOTONIC, &end_time);

        elapsed_time = (end_time.tv_sec - start_time.tv_sec) +
                   (double)(end_time.tv_nsec - start_time.tv_nsec) / 1000000000.0;

        printf("Elapsed time: %f seconds\n", elapsed_time);
    }

    // Release the GPIO line and close the chip device
    gpiod_line_release(line);
    gpiod_chip_close(chip);

    return 0;
}
