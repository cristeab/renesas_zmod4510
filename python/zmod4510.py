#!/usr/bin/env python3
# ZMOD4510 Air Quality Sensor Interface using ctypes

import ctypes
from enum import IntEnum
from pathlib import Path
import logging
import os


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
    def __init__(self, library_name="libzmod4510.so", logger=None, log_level=logging.INFO):
        self.logger = logger or logging.getLogger(__name__)
        logging.basicConfig(level=log_level)

        try:
            library_path = os.path.join(os.path.dirname(__file__), "lib", library_name)
            self.lib = ctypes.CDLL(library_path)
        except OSError as e:
            self.logger.error(f"Failed to load library: {e}")
            return
        
        # Define function signatures
        self.lib.sensor_init.restype = ctypes.c_int
        
        self.lib.sensor_step.argtypes = [ctypes.c_float, ctypes.c_float, ctypes.POINTER(SensorResults)]
        self.lib.sensor_step.restype = ctypes.c_int
        
        self.lib.sensor_close.restype = None

    def start(self):
        res = self.lib.sensor_init()
        if res != 0:
            self.logger.error(f"Sensor Init Failed with code {res}")
            return False
        return True

    def get_data(self, temperature, humidity):
        results = SensorResults()
        self.lib.sensor_step(temperature, humidity, ctypes.byref(results))
        return results

    def stop(self):
        self.lib.sensor_close()

# --- Main Python Execution Loop ---
if __name__ == "__main__":
    sensor = ZMOD4510()
    
    try:
        if not sensor.start():
            raise RuntimeError("Failed to start sensor.")
        sensor.logger.info("Sensor started. Press Ctrl+C to stop.")
        
        while True:
            # Example: You could get real T/RH from another Python library here
            current_temp = -300 
            current_rh = 50
            
            data = sensor.get_data(current_temp, current_rh)
            
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
