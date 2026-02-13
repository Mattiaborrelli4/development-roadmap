cmake_minimum_required(VERSION 3.15)
project(MemoryAllocator VERSION 1.0.0 LANGUAGES CXX)

# C++17 richiesto
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Compiler flags
if(MSVC)
    add_compile_options(/W4 /O2)
else()
    add_compile_options(-Wall -Wextra -O2)
endif()

# Definisci DEBUG mode per build Debug
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -DDEBUG_MODE")

# Eseguibile principale
add_executable(allocator
    src/allocator.cpp
    src/pool.cpp
    src/main.cpp
)

# Include directories
target_include_directories(allocator PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include)

# Posizione degli output
set_target_properties(allocator PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
)

# Install rules (opzionale)
install(TARGETS allocator DESTINATION bin)

# Print configuration
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "C++ Standard: ${CMAKE_CXX_STANDARD}")
