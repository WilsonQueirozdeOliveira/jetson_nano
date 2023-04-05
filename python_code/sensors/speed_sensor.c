#include <stdio.h>
#include <gpiod.h>
#include <pthread.h>
#include <time.h>
#include <math.h>
#include <errno.h>

double wheel_time_1 = 0;
double wheel_time_2 = 0;

double all_wheel_time = 0;

double tire_diameter = 0.067;

struct gpiod_chip *chip_1;
struct gpiod_chip *chip_2;

struct gpiod_line *line_1;
struct gpiod_line *line_2;

struct gpiod_line_event event;
int ret;

void delay(int milliseconds) {
    clock_t start_time = clock(); // get the starting clock time
    while (clock() < start_time + milliseconds); // loop until the specified delay has passed
}

void* wheel_timer_1(void* arg) {

   int pin_1 = 194;
   //int pin_2 = 149;

   // Open the GPIO chip device
   chip_1 = gpiod_chip_open_by_number(0);
   if (!chip_1) {
      printf("Failed to open GPIO chip\n");
   }

   // Request the GPIO line 
   line_1 = gpiod_chip_get_line(chip_1, pin_1);
   if (!line_1) {
      printf("Failed to get GPIO line\n");
   }

   // Configure the line for input and rising-edge interrupt events
   ret = gpiod_line_request_rising_edge_events(line_1, "my_program");
   if (ret < 0) {
      perror("Failed to request GPIO interrupt events\n");
      printf("Error: %d \n",errno);
      printf("pin: %d", pin_1);
   
      gpiod_line_release(line_1);
      gpiod_chip_close(chip_1);
   }

   printf("f1    ");

   struct timespec start_time, end_time;
   double elapsed_time;
  
   clock_gettime(CLOCK_MONOTONIC, &start_time);

   ret = gpiod_line_event_wait(line_1, NULL);
   if (ret < 0) {
      printf("Failed to wait for GPIO events\n");
   }
   ret = gpiod_line_event_read(line_1, &event);
   if (ret < 0) {
      printf("Failed to read GPIO events\n");
   }

   clock_gettime(CLOCK_MONOTONIC, &end_time);

   elapsed_time = (end_time.tv_sec - start_time.tv_sec) +
               (double)(end_time.tv_nsec - start_time.tv_nsec) / 1000000000.0;

   printf("Elapsed time : %f seconds\n", elapsed_time);

   wheel_time_1 = elapsed_time;
   printf("wheel_time_1: %0.7f \n ",(float)wheel_time_1);
   return NULL;

}

void wheel_timer_11(void) {

   int pin_1 = 194;
   //int pin_2 = 149;

   // Open the GPIO chip device
   chip_1 = gpiod_chip_open_by_number(0);
   if (!chip_1) {
      printf("Failed to open GPIO chip\n");
   }

   // Request the GPIO line 
   line_1 = gpiod_chip_get_line(chip_1, pin_1);
   if (!line_1) {
      printf("Failed to get GPIO line\n");
   }

   // Configure the line for input and rising-edge interrupt events
   ret = gpiod_line_request_rising_edge_events(line_1, "my_program");
   if (ret < 0) {
      perror("Failed to request GPIO interrupt events\n");
      printf("Error: %d \n",errno);
      printf("pin: %d", pin_1);
   }

   printf("    f1    ");

   struct timespec start_time, end_time;
   double elapsed_time;
  
   clock_gettime(CLOCK_MONOTONIC, &start_time);

   ret = gpiod_line_event_wait(line_1, NULL);
   if (ret < 0) {
      printf("Failed to wait for GPIO events\n");
   }
   ret = gpiod_line_event_read(line_1, &event);
   if (ret < 0) {
      printf("Failed to read GPIO events\n");
   }

   clock_gettime(CLOCK_MONOTONIC, &end_time);

   elapsed_time = (end_time.tv_sec - start_time.tv_sec) +
               (double)(end_time.tv_nsec - start_time.tv_nsec) / 1000000000.0;

   printf("Elapsed time : %f seconds\n", elapsed_time);

   wheel_time_1 = elapsed_time;
   printf("wheel_time_1: %0.7f \n ",(float)wheel_time_1);

}

void* wheel_timer_2(void* arg) {

   int pin_2 = 149;

   // Open the GPIO chip device
   chip_2 = gpiod_chip_open_by_number(0);
   if (!chip_2) {
      printf("Failed to open GPIO chip\n");
   }

   // Request the GPIO line 
   line_2 = gpiod_chip_get_line(chip_2, pin_2);
   if (!line_2) {
      printf("Failed to get GPIO line\n");
   }

   // Configure the line for input and rising-edge interrupt events
   ret = gpiod_line_request_rising_edge_events(line_2, "my_program");
   if (ret < 0) {
      perror("Failed to request GPIO interrupt events\n");
      printf("Error: %d \n",errno);
      printf("pin: %d", pin_2);

   }
   printf("f2    ");

   struct timespec start_time, end_time;
   double elapsed_time;
   
   clock_gettime(CLOCK_MONOTONIC, &start_time);

   ret = gpiod_line_event_wait(line_2, NULL);
   if (ret < 0) {
      printf("Failed to wait for GPIO events\n");
   }
   ret = gpiod_line_event_read(line_2, &event);
   if (ret < 0) {
      printf("Failed to read GPIO events\n");
   }

   clock_gettime(CLOCK_MONOTONIC, &end_time);

   elapsed_time = (end_time.tv_sec - start_time.tv_sec) +
               (double)(end_time.tv_nsec - start_time.tv_nsec) / 1000000000.0;

   printf("Elapsed time : %f seconds\n", elapsed_time);

   wheel_time_2 = elapsed_time;
   printf("wheel_time_2: %0.7f \n ",(float)wheel_time_2);
   return NULL; 
}

void wheel_timer_22(void) {

   int pin_2 = 149;

   // Open the GPIO chip device
   chip_2 = gpiod_chip_open_by_number(0);
   if (!chip_2) {
      printf("Failed to open GPIO chip\n");
   }

   // Request the GPIO line 
   line_2 = gpiod_chip_get_line(chip_2, pin_2);
   if (!line_2) {
      printf("Failed to get GPIO line\n");
   }

   // Configure the line for input and rising-edge interrupt events
   ret = gpiod_line_request_rising_edge_events(line_2, "my_program");
   if (ret < 0) {
      perror("Failed to request GPIO interrupt events\n");
      printf("Error: %d \n",errno);
      printf("pin: %d", pin_2);

      
      gpiod_line_release(line_2);
      gpiod_chip_close(chip_2);
   }

   printf("    f2    ");

   struct timespec start_time, end_time;
   double elapsed_time;
   
   clock_gettime(CLOCK_MONOTONIC, &start_time);

   ret = gpiod_line_event_wait(line_2, NULL);
   if (ret < 0) {
      perror("Failed to wait for GPIO events\n");
      printf("Error: %d \n",errno);
      
   }
   ret = gpiod_line_event_read(line_2, &event);
   if (ret < 0) {
      printf("Failed to read GPIO events\n");
   }

   clock_gettime(CLOCK_MONOTONIC, &end_time);

   elapsed_time = (end_time.tv_sec - start_time.tv_sec) +
               (double)(end_time.tv_nsec - start_time.tv_nsec) / 1000000000.0;

   printf("Elapsed time : %f seconds\n", elapsed_time);

   wheel_time_2 = elapsed_time;
   printf("wheel_time_2: %0.7f \n ",(float)wheel_time_2);
    
}

void threads_read(){

   printf("%s \n","oi..........................................................................");

   pthread_t thread_id1, thread_id2;

   pthread_create(&thread_id1, NULL, wheel_timer_1, NULL);
   pthread_create(&thread_id2, NULL, wheel_timer_2, NULL);

   pthread_join(thread_id1, NULL);
   pthread_join(thread_id2, NULL);

   //gpiod_line_release(line_1);
   //gpiod_chip_close(chip_1);

   //gpiod_line_release(line_2);
   //gpiod_chip_close(chip_2);

}

// Function to get the current speed
float get_speed() {

   printf("....oi...."); 

   //threads_read();

   wheel_timer_22();

   wheel_timer_11();
   

   gpiod_line_release(line_1);
   gpiod_chip_close(chip_1);

   gpiod_line_release(line_2);
   gpiod_chip_close(chip_2);

   printf("....fui....");

   //all_wheel_time = (wheel_time_1+wheel_time_2)/2.0;
   float speed = all_wheel_time;

   return speed;
}

int main() {
   return 0;
}