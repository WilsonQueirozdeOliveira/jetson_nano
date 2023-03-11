#include <stdio.h>
#include <stdlib.h>
#include <gpiod.h>
#include <signal.h>
#include <time.h>
#include <unistd.h>

volatile sig_atomic_t stop;

void interrupt_handler(struct gpiod_line_event event, void *data)
{
    printf("Interrupt occurred!\n");
}

void handle_signal(int sig)
{
    stop = 1;
}

int main()
{
    struct gpiod_chip *chip;
    struct gpiod_line *line;

    int req_flag = GPIOD_LINE_REQUEST_DIRECTION_INPUT;
    int line_num = 194; // 40-PIN GPIO 15
    int ret;

    struct gpiod_line_request_config config;
    config.consumer = "my_interrupt_handler";
    config.request_type = GPIOD_LINE_REQUEST_EVENT_RISING_EDGE;
    config.flags = 0;

    struct gpiod_line_event event;

    int count = 0;

    // Open the GPIO chip
    chip = gpiod_chip_open("/dev/gpiochip0");
    if (!chip) {
        perror("Error opening GPIO chip");
        exit(EXIT_FAILURE);
    }

    // Get the GPIO line
    line = gpiod_chip_get_line(chip, line_num);
    if (!line) {
        perror("Error getting GPIO line");
        exit(EXIT_FAILURE);
    }

    // Request the GPIO line
    ret = gpiod_line_request(line, &config, req_flag);
    if (ret < 0) {
        perror("Error requesting GPIO line");
        exit(EXIT_FAILURE);
    }

    // Configure the interrupt handler
    gpiod_line_event_wait(line, NULL);

    // Register signal handler to stop the loop
    signal(SIGINT, handle_signal);

    // Wait for an interrupt to occur
    printf("Waiting for interrupt...\n");
    while (!stop) {
        count++;
        printf("count: %i\n",count);

        ret = gpiod_line_event_wait(line, NULL);
        if (ret < 0) {
            perror("Error waiting for GPIO event");
            break;
        }
        
        ret = gpiod_line_event_read(line, &event);
        if (ret != 0) {
            perror("Error reading GPIO event");
            break;
        }
        printf("Interrupt occurred!\n");
        if(count > 30){
            break;
        }
    }

    // Cleanup
    gpiod_line_release(line);
    gpiod_chip_close(chip);

    return 0;
}
