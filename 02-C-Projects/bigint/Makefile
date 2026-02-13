# Makefile per BigInt Library

CC = gcc
CFLAGS = -Wall -Wextra -O2 -std=c99
TARGET = bigint
OBJS = bigint.o main.o

# Target principale
all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJS)

bigint.o: bigint.c bigint.h
	$(CC) $(CFLAGS) -c bigint.c

main.o: main.c bigint.h
	$(CC) $(CFLAGS) -c main.c

# Esegue i test
test: $(TARGET)
	./$(TARGET)

# Modalità interattiva
interactive: $(TARGET)
	./$(TARGET) -i

# Pulizia
clean:
	del $(OBJS) $(TARGET) 2>nul || rm -f $(OBJS) $(TARGET)

# Compilazione con debug
debug: CFLAGS += -g -DDEBUG
debug: clean $(TARGET)

# Phony targets
.PHONY: all test interactive clean debug
