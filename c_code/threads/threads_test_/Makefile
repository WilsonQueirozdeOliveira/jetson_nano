CC=gcc
CFLAGS=-Wall -Wextra -pthread

all: threads_test

threads_test: threads_test.c
	$(CC) $(CFLAGS) threads_test.c -o threads_test

clean:
	rm -f threads_test
