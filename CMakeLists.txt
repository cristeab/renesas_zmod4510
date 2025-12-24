cmake_minimum_required(VERSION 3.0)
project(no2_o3-example)

# Set C standard
set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_INCLUDE_CURRENT_DIR ON)

# Sources
set(SOURCES
    example.c
    sensors/zmod4xxx.c
    sensors/hs4xxx.c
    sensors/hs3xxx.c
    sensors/hsxxxx.c
    hal/zmod4xxx_hal.c
    hal/hal.c
    hal/raspi/rpi.c
)

# Add executable
add_executable(${PROJECT_NAME} ${SOURCES})

# Include directories
target_include_directories(${PROJECT_NAME} PRIVATE
    algos sensors hal)

# Link libraries directly
target_link_directories(${PROJECT_NAME} PRIVATE
    "${CMAKE_CURRENT_SOURCE_DIR}/../lib/Raspberry Pi/ARMv8-A x64/aarch64-linux-gnu-gcc")
target_link_libraries(${PROJECT_NAME}
    _no2_o3.a
    _zmod4xxx_cleaning.a
    m)
