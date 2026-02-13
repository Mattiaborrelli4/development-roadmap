cmake_minimum_required(VERSION 3.10)
project(RegexEngine VERSION 1.0 LANGUAGES CXX)

# Imposta standard C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Imposta warnings
if(MSVC)
    add_compile_options(/W4)
else()
    add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# File sorgenti
set(SOURCES
    regex.cpp
    nfa.cpp
    dfa.cpp
)

# File headers
set(HEADERS
    regex.h
    nfa.h
    dfa.h
)

# Crea eseguibile
add_executable(regex
    ${SOURCES}
    main.cpp
)

# Includi directory corrente per headers
target_include_directories(regex PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

# Imposta nome output in base al sistema
if(WIN32)
    set_target_properties(regex PROPERTIES OUTPUT_NAME regex)
endif()

# Opzione per build con debug symbols
option(BUILD_DEBUG "Build with debug symbols" OFF)
if(BUILD_DEBUG)
    target_compile_definitions(regex PRIVATE DEBUG_BUILD)
endif()

# Installazione (opzionale)
install(TARGETS regex
    RUNTIME DESTINATION bin
)

# Informazioni di build
message(STATUS "")
message(STATUS "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
message(STATUS "  Regex Engine Configuration")
message(STATUS "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
message(STATUS "  C++ Standard:    ${CMAKE_CXX_STANDARD}")
message(STATUS "  Build Type:      ${CMAKE_BUILD_TYPE}")
message(STATUS "  Compiler:        ${CMAKE_CXX_COMPILER_ID}")
message(STATUS "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
message(STATUS "")
