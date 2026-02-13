cmake_minimum_required(VERSION 3.10)
project(DatabaseEngine VERSION 1.0 LANGUAGES CXX)

# Imposta standard C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Flag di compilazione
if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU" OR CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -O2")
elseif(MSVC)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /W4 /O2")
endif()

# File sorgenti
set(SOURCES
    main.cpp
    btree.cpp
    sql.cpp
    database.cpp
)

# File header
set(HEADERS
    btree.h
    sql.h
    database.h
)

# Eseguibile
add_executable(database_engine ${SOURCES} ${HEADERS})

# Imposta la cartella di output
set_target_properties(database_engine PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)

# Installazione (opzionale)
install(TARGETS database_engine DESTINATION bin)

# Copia il README nella cartella di build
configure_file(${CMAKE_SOURCE_DIR}/README.md ${CMAKE_BINARY_DIR}/README.md COPYONLY)
