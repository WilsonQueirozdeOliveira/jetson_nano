#include <stdio.h>
#include <gpiod.h>

int main(void) {
    struct gpiod_chip *chip;
    struct gpiod_line *line;
    int line_number = 194; //(194 LINUX = 22 BCM = 15 40-PIN HEADER) replace with the actual GPIO pin number you want to read

    chip = gpiod_chip_open_by_number(0); // use chip 0
    line = gpiod_chip_get_line(chip, line_number);
    gpiod_line_request_input(line, "read-gpio");

    int input_value = gpiod_line_get_value(line);

    printf("Input value: %d\n", input_value);

    gpiod_line_release(line);
    gpiod_chip_close(chip);

    return 0;
}
