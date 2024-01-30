
#include "open_interface.h"

double move_forward(oi_t*sensor_data, double distance_mm){

    double sum = 0;

    oi_setWheels(500, 500);

        while (sum < 1000) {

            oi_update(sensor_data);

            sum += sensor_data -> distance;
        }

    oi_setWheels(0,0);

}

double turn_right(oi_t*sensor, double degrees){

}

double turn_left(oi_t*sensor, double degrees){

}

