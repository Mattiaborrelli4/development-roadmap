// Test program for mydev character device driver
// Educational userspace application
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <sys/ioctl.h>
#include <sys/types.h>

#define DEVICE_PATH "/dev/mydev"
#define MYDEV_IOCTL_MAGIC 'M'
#define MYDEV_IOCTL_RESET _IO(MYDEV_IOCTL_MAGIC, 1)
#define MYDEV_IOCTL_GET_SIZE _IOR(MYDEV_IOCTL_MAGIC, 2, int)
#define MYDEV_IOCTL_CLEAR _IO(MYDEV_IOCTL_MAGIC, 3)

// Color codes for output
#define COLOR_GREEN "\033[0;32m"
#define COLOR_RED "\033[0;31m"
#define COLOR_YELLOW "\033[0;33m"
#define COLOR_BLUE "\033[0;34m"
#define COLOR_RESET "\033[0m"

// Test functions
int test_open_close(void);
int test_write_read(const char *test_data);
int test_large_write(void);
int test_ioctl_commands(void);
int test_multiple_operations(void);

void print_success(const char *msg);
void print_error(const char *msg);
void print_info(const char *msg);

int main(void)
{
    int failures = 0;

    printf("\n");
    printf("==============================================\n");
    printf("  Test Program: MyDev Character Device\n");
    printf("  Educational Kernel Module Testing\n");
    printf("==============================================\n\n");

    // Test 1: Open and close device
    print_info("Test 1: Open/Close device");
    if (test_open_close() != 0) {
        failures++;
        print_error("Test 1 FALLITO\n");
    } else {
        print_success("Test 1 SUPERATO\n");
    }

    // Test 2: Basic write and read
    print_info("Test 2: Write and Read");
    if (test_write_read("Ciao Kernel!") != 0) {
        failures++;
        print_error("Test 2 FALLITO\n");
    } else {
        print_success("Test 2 SUPERATO\n");
    }

    // Test 3: Large write (buffer size test)
    print_info("Test 3: Large write");
    if (test_large_write() != 0) {
        failures++;
        print_error("Test 3 FALLITO\n");
    } else {
        print_success("Test 3 SUPERATO\n");
    }

    // Test 4: IOCTL commands
    print_info("Test 4: IOCTL commands");
    if (test_ioctl_commands() != 0) {
        failures++;
        print_error("Test 4 FALLITO\n");
    } else {
        print_success("Test 4 SUPERATO\n");
    }

    // Test 5: Multiple operations
    print_info("Test 5: Multiple operations");
    if (test_multiple_operations() != 0) {
        failures++;
        print_error("Test 5 FALLITO\n");
    } else {
        print_success("Test 5 SUPERATO\n");
    }

    // Summary
    printf("\n");
    printf("==============================================\n");
    if (failures == 0) {
        print_success("Tutti i test SUPERATI!");
        printf("  Verifica /proc/mydev_stats per statistiche\n");
    } else {
        printf("Test falliti: %d\n", failures);
        print_error("Alcuni test sono falliti");
    }
    printf("==============================================\n\n");

    return failures > 0 ? 1 : 0;
}

int test_open_close(void)
{
    int fd;

    fd = open(DEVICE_PATH, O_RDWR);
    if (fd < 0) {
        perror("  [ERRORE] Impossibile aprire il device");
        return -1;
    }

    printf("  Device aperto correttamente (fd=%d)\n", fd);

    if (close(fd) < 0) {
        perror("  [ERRORE] Impossibile chiudere il device");
        return -1;
    }

    printf("  Device chiuso correttamente\n");
    return 0;
}

int test_write_read(const char *test_data)
{
    int fd;
    char buffer[1024];
    ssize_t ret;
    size_t data_len = strlen(test_data);

    fd = open(DEVICE_PATH, O_RDWR);
    if (fd < 0) {
        perror("  [ERRORE] Impossibile aprire il device");
        return -1;
    }

    // Write test data
    ret = write(fd, test_data, data_len);
    if (ret < 0) {
        perror("  [ERRORE] Write fallita");
        close(fd);
        return -1;
    }

    printf("  Scritti %zd byte: \"%s\"\n", ret, test_data);

    // Reset position for reading
    if (ioctl(fd, MYDEV_IOCTL_RESET) < 0) {
        perror("  [ERRORE] IOCTL RESET fallita");
        close(fd);
        return -1;
    }

    // Read back data
    memset(buffer, 0, sizeof(buffer));
    ret = read(fd, buffer, sizeof(buffer));
    if (ret < 0) {
        perror("  [ERRORE] Read fallita");
        close(fd);
        return -1;
    }

    printf("  Letti %zd byte: \"%s\"\n", ret, buffer);

    // Verify data
    if (strcmp(buffer, test_data) != 0) {
        printf("  [ERRORE] Dati non corrispondenti!\n");
        printf("  Atteso: \"%s\"\n", test_data);
        printf("  Ricevuto: \"%s\"\n", buffer);
        close(fd);
        return -1;
    }

    printf("  Dati verificati con successo\n");

    close(fd);
    return 0;
}

int test_large_write(void)
{
    int fd;
    char *large_data;
    char buffer[1024];
    ssize_t ret;
    size_t large_size = 2048; // Larger than buffer

    fd = open(DEVICE_PATH, O_RDWR);
    if (fd < 0) {
        perror("  [ERRORE] Impossibile aprire il device");
        return -1;
    }

    // Allocate large data
    large_data = malloc(large_size);
    if (!large_data) {
        perror("  [ERRORE] Malloc fallito");
        close(fd);
        return -1;
    }

    // Fill with pattern
    memset(large_data, 'A', large_size);
    large_data[large_size - 1] = '\0';

    // Write large data (should be truncated)
    ret = write(fd, large_data, large_size);
    if (ret < 0) {
        perror("  [ERRORE] Write fallita");
        free(large_data);
        close(fd);
        return -1;
    }

    printf("  Scritti %zd byte (buffer limit: 1024)\n", ret);

    // Get size via IOCTL
    int size = 0;
    if (ioctl(fd, MYDEV_IOCTL_GET_SIZE, &size) < 0) {
        perror("  [ERRORE] IOCTL GET_SIZE fallita");
    } else {
        printf("  Dimensione dati via IOCTL: %d byte\n", size);
    }

    free(large_data);
    close(fd);
    return 0;
}

int test_ioctl_commands(void)
{
    int fd;
    int ret;

    fd = open(DEVICE_PATH, O_RDWR);
    if (fd < 0) {
        perror("  [ERRORE] Impossibile aprire il device");
        return -1;
    }

    // Test GET_SIZE on empty buffer
    int size = 0;
    ret = ioctl(fd, MYDEV_IOCTL_GET_SIZE, &size);
    if (ret < 0) {
        perror("  [ERRORE] IOCTL GET_SIZE fallita");
        close(fd);
        return -1;
    }
    printf("  IOCTL GET_SIZE: %d byte\n", size);

    // Write some data
    const char *test_msg = "Test IOCTL";
    write(fd, test_msg, strlen(test_msg));

    // Get size again
    ret = ioctl(fd, MYDEV_IOCTL_GET_SIZE, &size);
    if (ret < 0) {
        perror("  [ERRORE] IOCTL GET_SIZE fallita");
        close(fd);
        return -1;
    }
    printf("  IOCTL GET_SIZE dopo write: %d byte\n", size);

    // Test RESET
    ret = ioctl(fd, MYDEV_IOCTL_RESET);
    if (ret < 0) {
        perror("  [ERRORE] IOCTL RESET fallita");
        close(fd);
        return -1;
    }
    printf("  IOCTL RESET eseguito\n");

    // Test CLEAR
    ret = ioctl(fd, MYDEV_IOCTL_CLEAR);
    if (ret < 0) {
        perror("  [ERRORE] IOCTL CLEAR fallita");
        close(fd);
        return -1;
    }
    printf("  IOCTL CLEAR eseguito\n");

    // Verify cleared
    ret = ioctl(fd, MYDEV_IOCTL_GET_SIZE, &size);
    if (ret < 0 || size != 0) {
        printf("  [ERRORE] Buffer non pulito correttamente\n");
        close(fd);
        return -1;
    }
    printf("  IOCTL CLEAR verificato: size=%d\n", size);

    close(fd);
    return 0;
}

int test_multiple_operations(void)
{
    int fd;
    char buffer[256];
    int i;

    fd = open(DEVICE_PATH, O_RDWR);
    if (fd < 0) {
        perror("  [ERRORE] Impossibile aprire il device");
        return -1;
    }

    // Perform multiple write/read cycles
    printf("  Esecuzione di 5 cicli write/read...\n");

    for (i = 1; i <= 5; i++) {
        char msg[64];
        ssize_t ret;

        snprintf(msg, sizeof(msg), "Messaggio #%d", i);

        // Write
        ret = write(fd, msg, strlen(msg));
        if (ret < 0) {
            perror("  [ERRORE] Write fallita");
            close(fd);
            return -1;
        }

        // Reset
        ioctl(fd, MYDEV_IOCTL_RESET);

        // Read
        memset(buffer, 0, sizeof(buffer));
        ret = read(fd, buffer, sizeof(buffer));
        if (ret < 0) {
            perror("  [ERRORE] Read fallita");
            close(fd);
            return -1;
        }

        printf("  Ciclo %d: \"%s\"\n", i, buffer);
    }

    close(fd);
    return 0;
}

void print_success(const char *msg)
{
    printf(COLOR_GREEN "[SUCCESSO] %s" COLOR_RESET "\n", msg);
}

void print_error(const char *msg)
{
    printf(COLOR_RED "[ERRORE] %s" COLOR_RESET "\n", msg);
}

void print_info(const char *msg)
{
    printf(COLOR_BLUE "[INFO] %s" COLOR_RESET "\n", msg);
}
