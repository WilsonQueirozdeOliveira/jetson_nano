#include <stdio.h>
#include <gpiod.h>
#include <pthread.h>
#include <time.h>
#include <math.h>

double wheel_time_1 = 0;
double wheel_time_2 = 0;
double all_wheel_time = 0;
double tire_diameter = 0.067;

struct gpiod_chip *chip;
struct gpiod_line *line;
struct gpiod_line_event event;
int ret;

struct timespec start_time, end_time;
double elapsed_time;

void delay(int milliseconds) {
    clock_t start_time = clock(); // get the starting clock time
    while (clock() < start_time + milliseconds); // loop until the specified delay has passed
}

// read gpio

double read_gpio(int pin) {

   // Open the GPIO chip device
   chip = gpiod_chip_open_by_number(0);
   if (!chip) {
      printf("Failed to open GPIO chip\n");
   }

   // Request the GPIO line 
   line = gpiod_chip_get_line(chip, pin);
   if (!line) {
      printf("Failed to get GPIO line\n");
   }

   // Configure the line for input and rising-edge interrupt events
   ret = gpiod_line_request_rising_edge_events(line, "my_program");
   //ret = gpiod_line_request(line, &config, req_flag);
   if (ret < 0) {
      printf("Failed to request GPIO interrupt events\n");
      gpiod_line_release(line);
      gpiod_chip_close(chip);
   }


   // if pin 29(linux149)= up counter1++
   int counter = 0;
   while(counter) {
      counter++;
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

      elapsed_time = (end_time.tv_sec - start_time.tv_sec) +
                  (double)(end_time.tv_nsec - start_time.tv_nsec) / 1000000000.0;

      printf("Elapsed time : %f seconds\n", elapsed_time);
   }
   return elapsed_time;
}

void* wheel_timer_1(void* arg) {
   wheel_time_1 = read_gpio(194);
   printf("wheel_time_1: %0.7f \n ",(float)wheel_time_1);
   return NULL;

}

void* wheel_timer_2(void* arg) {
   wheel_time_2 = read_gpio(149);
   printf("wheel_time_2: %0.7f \n ",(float)wheel_time_2);
   return NULL;
}

void threads_read(){

   printf("%s \n","oi..........................................................................");

   pthread_t thread_id1, thread_id2;

   pthread_create(&thread_id1, NULL, wheel_timer_1, NULL);
   pthread_create(&thread_id2, NULL, wheel_timer_2, NULL);

   pthread_join(thread_id1, NULL);
   pthread_join(thread_id2, NULL);

}

// Function to get the current speed
float get_speed() {
   //float speed = 42.0; // Replace with actual speed calculation
   threads_read();
   all_wheel_time = (wheel_time_1+wheel_time_1)/2.0;
   float speed = all_wheel_time ;
   return speed;
}

int main() {
   /*
   printf("%s \n","oi..........................................................................");

   pthread_t thread_id1, thread_id2;

   pthread_create(&thread_id1, NULL, wheel_timer_1, NULL);
   pthread_create(&thread_id2, NULL, wheel_timer_2, NULL);

   pthread_join(thread_id1, NULL);
   pthread_join(thread_id2, NULL);

   gpiod_line_release(line);
   gpiod_chip_close(chip);
   */
   return 0;
}