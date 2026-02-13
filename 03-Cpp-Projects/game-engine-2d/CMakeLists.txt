cmake_minimum_required(VERSION 3.10)
project(GameEngine2D)

# C++17 richiesto
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Compiler flags
if(MSVC)
    add_compile_options(/W4)
else()
    add_compile_options(-Wall -Wextra -pedantic)
endif()

# Executable
add_executable(game
    main.cpp
)

# Link Windows kernel32 per console API
if(WIN32)
    target_link_libraries(game kernel32)
endif()

# Output directory
set_target_properties(game PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)
