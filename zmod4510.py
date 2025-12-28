#!/usr/bin/env python3
# ZMOD4510 Air Quality Sensor Interface using ctypes

import ctypes
from enum import IntEnum
from pathlib import Path
import logging


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
    def __init__(self, library_path="./libzmod4510.so", logger=None, log_level=logging.INFO):
        self.logger = logger or logging.getLogger(__name__)
        logging.basicConfig(level=log_level)

        try:
            self.lib = ctypes.CDLL(str(Path(library_path).absolute()))
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
        res = self.lib.sensor_step(temperature, humidity, ctypes.byref(results))
        if res != 0:
            self.logger.warning(f"Warning: Measurement step failed ({res})")
        return results

    def stop(self):
        self.lib.sensor_close()

# --- Main Python Execution Loop ---
if __name__ == "__main__":
    sensor = ZMOD4510()
    
    try:
        if not sensor.start():
            raise RuntimeError("Failed to start sensor.")
        logger.info("Sensor started. Press Ctrl+C to stop.")
        
        while True:
            # Example: You could get real T/RH from another Python library here
            current_temp = -300 
            current_rh = 50
            
            data = sensor.get_data(current_temp, current_rh)
            
            match data.status:
                case ZMODStatus.STABILIZATION:
                    logger.info("Warming up...")

                case ZMODStatus.OK:
                    logger.info(f"O3: {data.o3_ppb:.2f} ppb | NO2: {data.no2_ppb:.2f} ppb | "
                        f"Fast AQI: {data.fast_aqi} | EPA AQI: {data.epa_aqi}")

                case ZMODStatus.DAMAGE:
                    logger.error("Damaged.")
                case _:
                    logger.error(f"Unknown status: {data.status}")
            
    except KeyboardInterrupt:
        logger.info("\nStopping sensor...")
    finally:
        sensor.stop()
