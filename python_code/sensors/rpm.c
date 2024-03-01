#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include <math.h>
#include <stdio.h>

#define SENSOR_PIN 4 // Example GPIO pin number for the sensor

volatile int pulse_count = 0;

// Constants
const int pulses_per_revolution = 3;

// Use a fixed interval for calculations (e.g., 1000 ms)
#define CALCULATION_INTERVAL_MS 100

void pulse_interrupt(uint gpio, uint32_t events) {
    pulse_count++;
}

void calculate_rpm() {
    static absolute_time_t last_calculation_time = {0};

    // Only proceed if the interval has passed
    if (absolute_time_diff_us(last_calculation_time, get_absolute_time()) >= CALCULATION_INTERVAL_MS * 1000) {
        // Calculate RPM based on the pulses in the last interval
        float rpm = (pulse_count * 60000.0) / (pulses_per_revolution * CALCULATION_INTERVAL_MS);

        // Update display or print
        printf(" %.2f\n", rpm);

        // Reset pulse count for the next interval
        pulse_count = 0;

        // Update last calculation time
        last_calculation_time = get_absolute_time();
    }
}

int main() {
    stdio_init_all();
    gpio_init(SENSOR_PIN);
    gpio_set_dir(SENSOR_PIN, GPIO_IN);
    gpio_pull_up(SENSOR_PIN);

    const uint LED_PIN = PICO_DEFAULT_LED_PIN;
    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);

    // Setup interrupt on rising edge
    gpio_set_irq_enabled_with_callback(SENSOR_PIN, GPIO_IRQ_EDGE_RISE, true, &pulse_interrupt);

    while (true) {
        calculate_rpm();

        // LED blink logic as a simple indicator
        //gpio_put(LED_PIN, 1);
        //sleep_ms(250);
        //gpio_put(LED_PIN, 0);
        //sleep_ms(1000);
    }

    return 0;
}

