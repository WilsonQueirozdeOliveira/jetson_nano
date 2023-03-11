CC=gcc
CFLAGS=-c -Wall
LDFLAGS=-lgpiod -lpthread
SOURCES=threads_gpio_counter.c
OBJECTS=$(SOURCES:.c=.o)
EXECUTABLE=threads_gpio_counter

all: $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
	$(CC) $(OBJECTS) -o  $@ $(LDFLAGS)

.c.o:
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -rf $(OBJECTS) $(EXECUTABLE)
