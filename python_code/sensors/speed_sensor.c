#include <gpiod.h>
#include <stdio.h>
#include <unistd.h>
#include <time.h>

#define WHEEL_CIRCUMFERENCE  0.2108 // Updated wheel circumference in meters (0.067 dismeter)
#define TIMEOUT_MS 50

double calculate_speed(double time_interval, int sensor_read_points) {
    double distance = WHEEL_CIRCUMFERENCE;
    //double speed = (distance * sensor_read_points) / time_interval;
    double speed = (distance/4) / time_interval;
    if (speed > 10.0){
        speed = 10.0;
    }
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

    struct timespec timeout;
    timeout.tv_sec = TIMEOUT_MS / 1000;
    timeout.tv_nsec = (TIMEOUT_MS % 1000) * 1000000;

    while (1) {
        ret = gpiod_line_event_wait(line1, &timeout);
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
            } else if (count1 == 1) { //else if (count1 == 4)
                time_interval1 = current_time.tv_sec - start_time1.tv_sec + (current_time.tv_nsec - start_time1.tv_nsec) / 1e9;
                speed1 = calculate_speed(time_interval1, count1);
                count1 = 0;
            }
        }

        ret = gpiod_line_event_wait(line2, &timeout);
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
            } else if (count2 == 1) {//else if (count1 == 4)
                time_interval2 = current_time.tv_sec - start_time2.tv_sec + (current_time.tv_nsec - start_time2.tv_nsec) / 1e9;
                speed2 = calculate_speed(time_interval2, count2);
                count2 = 0;
            }
        }

        if (count1 == 0 && count2 == 0) {
            avg_speed = (speed1 + speed2) / 2.0;
            printf("Wheel 1 Speed: %.2lf m/s, Wheel 2 Speed: %.2lf m/s, Average Speed: %.2lf m/s\n", speed1, speed2, avg_speed);
            
        }
        if (count1 == 0) {
            //avg_speed = speed1;
            printf("Wheel 1 Speed: %.2lf m/s, Wheel 2 Speed: %.2lf m/s, Average Speed: %.2lf m/s\n", speed1, speed2, avg_speed);
            
        }

        if (count2 == 0) {
            //avg_speed = speed2;
            printf("Wheel 1 Speed: %.2lf m/s, Wheel 2 Speed: %.2lf m/s, Average Speed: %.2lf m/s\n", speed1, speed2, avg_speed);
            
        }

        clock_gettime(CLOCK_MONOTONIC, &current_time);
        double elapsed_time = (current_time.tv_sec - start_time1.tv_sec) + (current_time.tv_nsec - start_time1.tv_nsec) / 1e9;

        if (elapsed_time > 0.5) {
            avg_speed = 0;
            printf("Timeout reached. Average Speed: %.2lf m/s\n", avg_speed);
            count1 = 0;
            count2 = 0;
            clock_gettime(CLOCK_MONOTONIC, &start_time1); // Reset start_time1 for the next iteration
            clock_gettime(CLOCK_MONOTONIC, &start_time2); // Reset start_time2 for the next iteration
        }
        
    }
    gpiod_line_release(line1);
    gpiod_line_release(line2);
    gpiod_chip_close(chip);
    return 0;
}