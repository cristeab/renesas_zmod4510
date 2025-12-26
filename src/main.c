#include "sensor_interface.h"
#include <stdio.h>
#include <stdlib.h>

int main() {    
    int ret = sensor_init();
    if (ret) {
        return EXIT_FAILURE;
    }

    /* Set default values for temperature and humidity: These values will be used
     * if no sensor is detected or if reading the sensor fails. 
     * The temperature value of -300°C causes the algo to use the on-chip temperature
     * measurement of the gas sensor. However, an external temperature and humidity
     * sensor provides better accuracy and is the preferred input source. */
    float default_temperature = -300;
    float default_humidity    =  50;
    printf("Using on-chip temperature sensor and 50%% relative humidity!\n\n");

    sensor_results_t results;
    while ( 1 ) {
        sensor_step(default_temperature, default_humidity, &results);
    
        /* Check validity of the algorithm results. */
        switch (results.status) {
        case NO2_O3_STABILIZATION:
            /* The sensor should run for at least 50 cycles to stabilize.
             * Algorithm results obtained during this period SHOULD NOT be
             * considered as valid outputs! */
            printf("Warm-Up!\n");
            break;
        case NO2_O3_OK:
            printf("  O3_conc     = %8.3f ppb\n", results.o3_ppb);
            printf("  NO2_conc    = %8.3f ppb\n", results.no2_ppb);
            printf("  Fast AQI    = %8i\n", results.fast_aqi);
            printf("  EPA AQI     = %8i\n", results.epa_aqi);
            break;
        /* Notification from Sensor self-check. For more information, read the
         * Datasheet, section "Conditioning, Sensor Self-Check Status, and 
         * Stability". */
        case NO2_O3_DAMAGE:
            printf("Error: Sensor probably damaged. Algorithm results may be incorrect.\n");
            break;
        /* Exit program due to unexpected error. */
        default:
            printf("Unexpected status.\n");
            sensor_close();
            return EXIT_FAILURE;
        }
    }
    sensor_close();
    return EXIT_SUCCESS;
}
