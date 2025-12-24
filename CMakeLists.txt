cmake_minimum_required(VERSION 3.0)
project(no2_o3-example)

# Set C standard
set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)

# Sources
set(SOURCES
    src/main.c
    src/sensors/zmod4xxx.c
    src/hal/zmod4xxx_hal.c
    src/hal/hal.c
    src/hal/raspi/rpi.c
)

# Add executable
add_executable(${PROJECT_NAME} ${SOURCES})

# Include directories
target_include_directories(${PROJECT_NAME} PRIVATE
    src src/algos src/sensors src/hal)

# Link libraries directly
target_link_directories(${PROJECT_NAME} PRIVATE
    "${CMAKE_CURRENT_SOURCE_DIR}/lib")
target_link_libraries(${PROJECT_NAME}
    _no2_o3.a
    _zmod4xxx_cleaning.a
    m)
