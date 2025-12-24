# Renesas ZMOD4510 Sensor Firmware for Raspberry Pi5

This is a modified version of the firmware provided by Renesas for the ZMOD4510 O3 and NO2 sensor.
The following changes have been made:
- the dependency on PiGPIO library is removed, instead the Linux kernel's native I2C interface is used,
- the code related to temperature and relative humidity sensor is removed,
- the algorithm libraries are provided only for Raspberry Pi,
- cmake is used for compilation management

# Compilation Instructions

    cmake -S . -B build
    cmake --build build

Run the generated binary with:

    build/no2_o3-example

