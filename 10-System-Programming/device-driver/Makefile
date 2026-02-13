# Makefile for mydev kernel module
# Educational character device driver

# Module name
obj-m += mydev.o

# Kernel build directory
KDIR := /lib/modules/$(shell uname -r)/build

# Current directory
PWD := $(shell pwd)

# Default target
all:
	$(MAKE) -C $(KDIR) M=$(PWD) modules

# Clean build artifacts
clean:
	$(MAKE) -C $(KDIR) M=$(PWD) clean
	rm -f test
	rm -f Module.symvers modules.order

# Install module (optional)
install:
	$(MAKE) -C $(KDIR) M=$(PWD) modules_install
	depmod -a

# Build test program
test: mydev.ko test.c
	$(CC) -o test test.c -Wall -Wextra

# Help message
help:
	@echo "Target disponibili:"
	@echo "  make          - Compila il modulo kernel"
	@echo "  make clean    - Rimuovi i file di compilazione"
	@echo "  make test     - Compila il programma di test"
	@echo "  make install  - Installa il modulo (richiede root)"
	@echo ""
	@echo "Utilizzo:"
	@echo "  1. make               # Compila il modulo"
	@echo "  2. sudo insmod mydev.ko   # Carica il modulo"
	@echo "  3. sudo ./test        # Esegui il test"
	@echo "  4. cat /proc/mydev_stats  # Vedi statistiche"
	@echo "  5. sudo rmmod mydev   # Scarica il modulo"

.PHONY: all clean install help
