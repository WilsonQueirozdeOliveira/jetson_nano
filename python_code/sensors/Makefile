CC=gcc
CFLAGS=-Wall -shared -fPIC

LDFLAGS=-shared -fPIC -lgpiod -lpthread 

all: c_speed_sensor.so

c_speed_sensor.so: speed_sensor.c
	$(CC) $(CFLAGS) $(LDFLAGS) $^ -o $@ -lgpiod

clean:
	rm -f c_speed_sensor.so
