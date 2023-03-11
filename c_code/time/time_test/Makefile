CC=gcc
CFLAGS=-c -Wall
LDFLAGS=
SOURCES=time_test.c
OBJECTS=$(SOURCES:.c=.o)
EXECUTABLE=time_test

all: $(SOURCES) $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
	$(CC) $(LDFLAGS) $(OBJECTS) -o $@

.c.o:
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -f $(OBJECTS) $(EXECUTABLE)
