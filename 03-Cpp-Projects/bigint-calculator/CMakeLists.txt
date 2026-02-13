# CMakeLists.txt per BigInt Calculator
# Minima versione richiesta
cmake_minimum_required(VERSION 3.10)

# Nome del progetto
project(BigIntCalculator VERSION 1.0 LANGUAGES CXX)

# Standard C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Flag di compilazione
if(MSVC)
    add_compile_options(/W4)
else()
    add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Flag di ottimizzazione per Release
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O2")

# Sorgenti
set(SOURCES
    bigint.cpp
    main.cpp
)

# Intestazioni
set(HEADERS
    bigint.h
)

# Eseguibile
add_executable(bigint_calc ${SOURCES} ${HEADERS})

# Se presenti, permetti di runnare i test con make test
enable_testing()

# Installazione (opzionale)
install(TARGETS bigint_calc
    RUNTIME DESTINATION bin
)

# Mostra informazioni di build
message(STATUS "")
message(STATUS "=== BigInt Calculator ===")
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "C++ Standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "Compiler: ${CMAKE_CXX_COMPILER_ID} ${CMAKE_CXX_COMPILER_VERSION}")
message(STATUS "=========================")
message(STATUS "")
