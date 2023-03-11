CC = gcc
CFLAGS = -Wall
LIBS = -lgpiod

PROG = interrupt

all: $(PROG)

$(PROG): $(PROG).c
	$(CC) $(CFLAGS) -o $@ $< $(LIBS)

clean:
	rm -f $(PROG)