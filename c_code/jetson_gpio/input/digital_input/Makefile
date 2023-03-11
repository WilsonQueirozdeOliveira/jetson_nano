CC=gcc
CFLAGS=-Wall -Wextra -Wpedantic
LDFLAGS=-lgpiod

digital_input: digital_input.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

clean:
	rm -f digital_input
	rm -f digital_input.o
