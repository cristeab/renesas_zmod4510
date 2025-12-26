#ifndef SENSOR_INTERFACE_H
#define SENSOR_INTERFACE_H

#include "no2_o3.h"

typedef struct {
    float o3_ppb;
    float no2_ppb;
    int32_t fast_aqi;
    int32_t epa_aqi;
    int32_t status; // To return NO2_O3_OK, etc.
} sensor_results_t;

int sensor_init();
void sensor_step(float temp, float humidity, sensor_results_t* out);
void sensor_close();

#endif