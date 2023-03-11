CC=gcc
CFLAGS=-Wall -Wextra
LDFLAGS=-lgpiod
SRC=up_edge.c
OBJ=$(SRC:.c=.o)
EXEC=up_edge

all: $(EXEC)

$(EXEC): $(OBJ)
	$(CC) $(OBJ) -o $@ $(LDFLAGS)

%.o: %.c
	$(CC) -c $< -o $@ $(CFLAGS)

clean:
	rm -f $(OBJ) $(EXEC)
