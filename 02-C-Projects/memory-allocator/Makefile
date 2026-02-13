# Makefile per Memory Allocator
CC = gcc
CFLAGS = -Wall -Wextra -std=c99
TARGET = allocator_test
OBJS = allocator.o test.o

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJS)

allocator.o: allocator.c
	$(CC) $(CFLAGS) -c allocator.c

test.o: test.c
	$(CC) $(CFLAGS) -c test.c

test: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(OBJS) $(TARGET)

.PHONY: all test clean
