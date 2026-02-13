#!/bin/bash
# Build and Test Script for MyDev Device Driver
# Educational character device driver

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

MODULE_NAME="mydev"
DEVICE_NAME="mydev"
PROC_NAME="mydev_stats"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  MyDev Device Driver - Build & Test${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if running as root for module operations
if [ "$EUID" -ne 0 ]; then
    echo -e "${YELLOW}Nota: Alcune operazioni richiedono sudo${NC}"
fi

# Step 1: Build module
echo -e "${BLUE}[1/6] Building kernel module...${NC}"
make
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Module built successfully${NC}"
else
    echo -e "${RED}✗ Build failed${NC}"
    exit 1
fi
echo ""

# Step 2: Build test program
echo -e "${BLUE}[2/6] Building test program...${NC}"
make test
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Test program built successfully${NC}"
else
    echo -e "${RED}✗ Test build failed${NC}"
    exit 1
fi
echo ""

# Step 3: Load module
echo -e "${BLUE}[3/6] Loading kernel module...${NC}"
sudo insmod ${MODULE_NAME}.ko
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Module loaded${NC}"
else
    echo -e "${RED}✗ Failed to load module${NC}"
    exit 1
fi
sleep 1
echo ""

# Step 4: Check kernel messages
echo -e "${BLUE}[4/6] Checking kernel messages...${NC}"
dmesg | tail -10
echo ""

# Step 5: Verify device and proc entries
echo -e "${BLUE}[5/6] Verifying device entries...${NC}"
if [ -e "/dev/${DEVICE_NAME}" ]; then
    echo -e "${GREEN}✓ Device file exists: /dev/${DEVICE_NAME}${NC}"
    ls -l /dev/${DEVICE_NAME}
else
    echo -e "${RED}✗ Device file not found${NC}"
fi

if [ -e "/proc/${PROC_NAME}" ]; then
    echo -e "${GREEN}✓ Proc entry exists: /proc/${PROC_NAME}${NC}"
else
    echo -e "${RED}✗ Proc entry not found${NC}"
fi
echo ""

# Step 6: Run tests
echo -e "${BLUE}[6/6] Running tests...${NC}"
echo -e "${YELLOW}----------------------------------------${NC}"
sudo ./test
echo -e "${YELLOW}----------------------------------------${NC}"
echo ""

# Show statistics
echo -e "${BLUE}Device Statistics:${NC}"
if [ -e "/proc/${PROC_NAME}" ]; then
    cat /proc/${PROC_NAME}
else
    echo -e "${RED}Cannot read /proc/${PROC_NAME}${NC}"
fi
echo ""

# Optional: Unload module?
echo -e "${YELLOW}Unload module now? (y/n)${NC}"
read -r answer
if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
    echo -e "${BLUE}Unloading module...${NC}"
    sudo rmmod ${MODULE_NAME}
    echo -e "${GREEN}✓ Module unloaded${NC}"
    echo ""
    echo -e "${BLUE}Final kernel messages:${NC}"
    dmesg | tail -5
else
    echo -e "${YELLOW}Module remains loaded${NC}"
    echo -e "To unload manually: sudo rmmod ${MODULE_NAME}"
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Test script completed!${NC}"
echo -e "${GREEN}========================================${NC}"
