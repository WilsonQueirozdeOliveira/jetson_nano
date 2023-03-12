CC = gcc
CFLAGS = -Wall
LDFLAGS =

TARGET = libpoint.so
SOURCES = point.c
OBJECTS = $(SOURCES:.c=.o)

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CC) $(LDFLAGS) -shared -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c -fPIC -o $@ $<

clean:
	rm -f $(OBJECTS) $(TARGET)
