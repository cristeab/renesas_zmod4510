# Renesas ZMOD4510 Sensor Firmware for Raspberry Pi5

This is a modified version of the firmware provided by Renesas for the ZMOD4510 O3 and NO2 sensor.
The following changes have been made:
- the dependency on PiGPIO library is removed, instead the Linux kernel's native I2C interface is used,
- the code related to temperature and relative humidity sensor is removed,
- the algorithm libraries are provided only for Raspberry Pi,
- cmake is used for compilation management

# Compile the Sample Application

From the sources root folder:

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
```

Run the generated binary with:

```bash
build/no2_o3-example
```

# Compile and Install the Python Module

* Optionally, create and activate a Python virtual environment

```bash
python3 -m venv .venv-test
source ./.venv-test/bin/activate
```

* Compile and install from the sources root folder

```bash
pip install .
```

* Verify that the Python module is installed

```bash
python3 -c "import zmod4510; print(zmod4510.__file__); s = zmod4510.ZMOD4510(); print(dir(s))"
```