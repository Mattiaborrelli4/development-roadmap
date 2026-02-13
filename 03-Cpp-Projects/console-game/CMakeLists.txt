# ============================================================================
# CMakeLists.txt per Snake Game
# ============================================================================
# Build configuration moderna usando CMake
# Per usarlo:
#   mkdir build && cd build
#   cmake ..
#   cmake --build .
# ============================================================================

# Versione minima di CMake
cmake_minimum_required(VERSION 3.10)

# Nome del progetto
project(SnakeGame VERSION 1.0 LANGUAGES CXX)

# Imposta standard C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Opzioni di compilazione
option(BUILD_TESTS "Build test suite" OFF)
option(ENABLE_WARNINGS "Enable all warnings" ON)

# Flag di compilazione
if(ENABLE_WARNINGS)
    if(MSVC)
        add_compile_options(/W4)
    else()
        add_compile_options(-Wall -Wextra -Wpedantic)
    endif()
endif()

# Eseguibile principale
add_executable(snake
    ConsoleGame.cpp
)

# Link libraries (nessuna per questo progetto semplice)
# target_link_libraries(snake PRIVATE ...)

# Installazione
install(TARGETS snake
    RUNTIME DESTINATION bin
)

# Informazioni di build
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "C++ compiler: ${CMAKE_CXX_COMPILER}")
message(STATUS "C++ standard: ${CMAKE_CXX_STANDARD}")

# Configurazione Debug/Release
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

# Flag specifici per Debug
set(CMAKE_CXX_FLAGS_DEBUG "-g -O0 -DDEBUG")

# Flag specifici per Release
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -DNDEBUG")

# Summary
message(STATUS "")
message(STATUS "========================================")
message(STATUS "  Snake Game - Configuration Summary   ")
message(STATUS "========================================")
message(STATUS "  Build Type: ${CMAKE_BUILD_TYPE}")
message(STATUS "  C++ Standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "  Compiler: ${CMAKE_CXX_COMPILER_ID}")
message(STATUS "  Install Prefix: ${CMAKE_INSTALL_PREFIX}")
message(STATUS "========================================")
message(STATUS "")
