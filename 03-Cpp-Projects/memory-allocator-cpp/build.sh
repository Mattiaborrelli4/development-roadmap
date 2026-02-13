#!/bin/bash
# Build script per Unix/Linux/macOS

echo "Building C++ Memory Allocator..."

# Create build directory
mkdir -p build
cd build

# Run CMake
echo "Running CMake..."
cmake .. -DCMAKE_BUILD_TYPE=Release

if [ $? -ne 0 ]; then
    echo "CMake configuration failed!"
    exit 1
fi

# Build
echo "Building..."
make -j$(nproc)

if [ $? -ne 0 ]; then
    echo "Build failed!"
    exit 1
fi

echo ""
echo "========================================"
echo "Build completato con successo!"
echo "Eseguibile: build/bin/allocator"
echo "========================================"

cd ..
