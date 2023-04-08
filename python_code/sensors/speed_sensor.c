#include <gpiod.h>
#include <stdio.h>
#include <unistd.h>
#include <time.h>

#define WHEEL_CIRCUMFERENCE 0.067 // Updated wheel circumference in meters

double calculate_speed(double time_interval, int sensor_read_points) {
    double distance = WHEEL_CIRCUMFERENCE;
    double speed = (distance * sensor_read_points) / time_interval;
    return speed;
}

double avg_speed = 0.0; // Declare avg_speed as a global variable

float get_speed() {
    return (float)avg_speed;
}

int main() {
    const char *chip_name = "gpiochip0";
    unsigned int pin_number1 = 149;
    unsigned int pin_number2 = 194;
    struct gpiod_chip *chip;
    struct gpiod_line *line1, *line2;
    struct gpiod_line_event event;
    int ret;

    struct timespec start_time1, start_time2, current_time;
    double time_interval1, time_interval2, speed1, speed2;
    int count1 = 0, count2 = 0;

    chip = gpiod_chip_open_by_name(chip_name);
    if (!chip) {
        perror("Open chip");
        return 1;
    }

    line1 = gpiod_chip_get_line(chip, pin_number1);
    line2 = gpiod_chip_get_line(chip, pin_number2);
    if (!line1 || !line2) {
        perror("Get lines");
        gpiod_chip_close(chip);
        return 1;
    }

    ret = gpiod_line_request_rising_edge_events(line1, "wheel_speed_example");
    if (ret < 0) {
        perror("Request rising edge events");
        gpiod_chip_close(chip);
        return 1;
    }

    ret = gpiod_line_request_rising_edge_events(line2, "wheel_speed_example");
    if (ret < 0) {
        perror("Request rising edge events");
        gpiod_chip_close(chip);
        return 1;
    }

    printf("Monitoring wheel speeds...\n");

    while (1) {
        ret = gpiod_line_event_wait(line1, NULL);
        if (ret < 0) {
            perror("Wait for events");
            break;
        } else if (ret > 0) {
            ret = gpiod_line_event_read(line1, &event);
            if (ret < 0) {
                perror("Read event");
                break;
            }

            clock_gettime(CLOCK_MONOTONIC, &current_time);

            count1++;
            if (count1 == 1) {
                start_time1 = current_time;
            } else if (count1 == 4) {
                time_interval1 = current_time.tv_sec - start_time1.tv_sec + (current_time.tv_nsec - start_time1.tv_nsec) / 1e9;
                speed1 = calculate_speed(time_interval1, count1);
                count1 = 0;
            }
        }

        ret = gpiod_line_event_wait(line2, NULL);
        if (ret < 0) {
            perror("Wait for events");
            break;
        } else if (ret > 0) {
            ret = gpiod_line_event_read(line2, &event);
            if (ret < 0) {
                perror("Read event");
                break;
            }

            clock_gettime(CLOCK_MONOTONIC, &current_time);

            count2++;
            if (count2 == 1) {
                start_time2 = current_time;
            } else if (count2 == 4) {
                time_interval2 = current_time.tv_sec - start_time2.tv_sec + (current_time.tv_nsec - start_time2.tv_nsec) / 1e9;
                speed2 = calculate_speed(time_interval2, count2);
                count2 = 0;
            }
        }

        if (count1 == 0 && count2 == 0) {
            avg_speed = (speed1 + speed2) / 2.0;
            printf("Wheel 1 Speed: %.2lf m/s, Wheel 2 Speed: %.2lf m/s, Average Speed: %.2lf m/s\n", speed1, speed2, avg_speed);
            break;
        }
        
    }
    gpiod_line_release(line1);
    gpiod_line_release(line2);
    gpiod_chip_close(chip);
    return 0;
}