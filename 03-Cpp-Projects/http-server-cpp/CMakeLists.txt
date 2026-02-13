cmake_minimum_required(VERSION 3.10)
project(HTTPServer VERSION 1.0 LANGUAGES CXX)

# C++17 required
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Source files
set(SOURCES
    server.cpp
    thread_pool.cpp
    main.cpp
)

# Headers
set(HEADERS
    server.h
    thread_pool.h
)

# Executable
add_executable(server ${SOURCES} ${HEADERS})

# Platform-specific libraries
if(WIN32)
    # Windows - Link Winsock2
    target_link_libraries(server ws2_32)
else()
    # Linux/Unix - Link pthread
    target_link_libraries(server pthread)
endif()

# Compiler warnings
if(MSVC)
    target_compile_options(server PRIVATE /W4)
else()
    target_compile_options(server PRIVATE -Wall -Wextra -pedantic)
endif()

# Installation
install(TARGETS server DESTINATION bin)
install(DIRECTORY public/ DESTINATION share/http-server/public)
