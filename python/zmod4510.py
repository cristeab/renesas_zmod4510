#!/usr/bin/env python3
# ZMOD4510 Air Quality Sensor Interface using ctypes

import ctypes
from enum import IntEnum
from pathlib import Path
import logging
import os
from ecomet_i2c_sensors.i2c import load_comet_yaml
from ecomet_i2c_sensors.zmod4510 import zmod4510_constant


class ZMODStatus(IntEnum):
    OK = 0
    STABILIZATION = 1
    DAMAGE = -102

# Define the Result Structure matching the C code
class SensorResults(ctypes.Structure):
    _fields_ = [
        ("o3_ppb", ctypes.c_float),
        ("no2_ppb", ctypes.c_float),
        ("fast_aqi", ctypes.c_int32),
        ("epa_aqi", ctypes.c_int32),
        ("status", ctypes.c_int32),
    ]

class ZMOD4510:
    def __init__(self, address=zmod4510_constant.ZMOD4510_ADDRESS, busnum=0, logger=None, log_level=logging.INFO):
        if i2c is None:
            import ecomet_i2c_sensors.i2c as I2C
            i2c = I2C
        self.logger = logger or logging.getLogger(__name__)    
        smb = load_comet_yaml()
        if smb != -99 :
           busnum = smb['i2c']['smb'].replace('i2c-', '')
        else :
           busnum = 0
        logging.basicConfig(level=log_level)
        self.busnum = int(busnum)

        try:
            library_path = os.path.join(os.path.dirname(__file__), "lib", "libzmod4510.so")
            self._lib = ctypes.CDLL(library_path)
        except OSError as e:
            self.logger.error(f"Failed to load library: {e}")
            raise
        
        # Define function signatures
        self._lib.sensor_init.restype = ctypes.c_int
        self._lib.sensor_init_with_bus.argtypes = [ctypes.c_int]
        self._lib.sensor_init_with_bus.restype = ctypes.c_int

        self._lib.sensor_step.argtypes = [ctypes.c_float, ctypes.c_float, ctypes.POINTER(SensorResults)]
        self._lib.sensor_step.restype = ctypes.c_int

        self._lib.sensor_close.restype = None

    def start(self):
        res = self._lib.sensor_init_with_bus(self.busnum)
        if res != 0:
            self.logger.error(f"Sensor Init Failed with code {res} (bus {self.busnum})")
            return False
        return True

    def get_data(self, temperature_celsius_deg = -300, relative_humidity_percent = 50):
        results = SensorResults()
        self._lib.sensor_step(temperature_celsius_deg, relative_humidity_percent, ctypes.byref(results))
        return results

    def stop(self):
        self._lib.sensor_close()


if __name__ == "__main__":
    sensor = ZMOD4510()
    
    try:
        if not sensor.start():
            raise RuntimeError("Failed to start sensor.")
        sensor.logger.info("Sensor started. Press Ctrl+C to stop.")
        
        while True:
            # Example: You could get real T/RH from another Python library here
            data = sensor.get_data()
            
            match data.status:
                case ZMODStatus.STABILIZATION:
                    sensor.logger.info("Warming up...")

                case ZMODStatus.OK:
                    sensor.logger.info(f"O3: {data.o3_ppb:.2f} ppb | NO2: {data.no2_ppb:.2f} ppb | "
                        f"Fast AQI: {data.fast_aqi} | EPA AQI: {data.epa_aqi}")

                case ZMODStatus.DAMAGE:
                    sensor.logger.error("Damaged.")
                case _:
                    sensor.logger.error(f"Unknown status: {data.status}")

    except KeyboardInterrupt:
        sensor.logger.info("\nStopping sensor...")
    finally:
        sensor.stop()
