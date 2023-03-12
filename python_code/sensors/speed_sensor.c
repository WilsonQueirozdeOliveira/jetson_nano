#include <stdio.h>
#include <gpiod.h>
#include <pthread.h>
#include <time.h>

double wheel_time_1 = 0;
double wheel_time_2 = 0;
double tire_diameter = 0.067;

// read gpio

double read_gpio(int pin) {

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

   // Request the GPIO line 
   line = gpiod_chip_get_line(chip, pin);
   if (!line) {
      printf("Failed to get GPIO line\n");
   }

   // Configure the line for input and rising-edge interrupt events
   ret = gpiod_line_request_rising_edge_events(line, "my_program");
   if (ret < 0) {
      printf("Failed to request GPIO interrupt events\n");
   }


   // if pin 29(linux149)= up counter1++
   while(true) {
      
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

   return elapsed_time_2;

}

// Function to get the current speed
float get_speed() {
   float speed = 42.0; // Replace with actual speed calculation
   return speed;
}

void* wheel_timer_1(void* arg) {
   wheel_time_1 = read_gpio(194);
   printf("wheel_time_2: %0.2f \n ",(float)wheel_time_2);
   return NULL;

}

void* wheel_timer_2(void* arg) {
   wheel_time_2 = read_gpio(149);
   printf("wheel_time_2: %0.2f \n ",(float)wheel_time_2);
   return NULL;
}



int main() {
   pthread_t thread_id1, thread_id2;

   pthread_create(&thread_id1, NULL, wheel_timer_1, NULL);
   pthread_create(&thread_id2, NULL, wheel_timer_1, NULL);

   pthread_join(thread_id1, NULL);
   pthread_join(thread_id2, NULL);


    return 0;
}