
#include "open_interface.h"
#include "lcd.h"

void turn_right(oi_t*sensor, double degrees){

    double sum = 0;

    oi_setWheels(-25, 25);

    while (sum < degrees-23){

        oi_update(sensor);

        sum += abs(sensor -> angle);


    }

    oi_setWheels(0, 0);
}


void turn_left(oi_t*sensor, double degrees){
    double sum = 0;

    oi_setWheels(25, -25);

    while (sum < degrees-23){
        oi_update(sensor);

        sum += abs(sensor -> angle);


       }

       oi_setWheels(0, 0);
}

double move_forward(oi_t*sensor_data, double distance_mm){

    double sum = 0;

    oi_setWheels(150, 150);

        while (sum < distance_mm) {

            oi_update(sensor_data);

            if ((sensor_data -> bumpLeft) || (sensor_data -> bumpRight)){
                oi_setWheels(0,0);
                return sum;
            }

            sum += sensor_data -> distance;

        }

    oi_setWheels(0,0);
    return sum;
}

double move_backward(oi_t*sensor_data, double distance_mm){

    double sum = 0;

    oi_setWheels(-150,-150);

    while (sum < distance_mm) {
        oi_update(sensor_data);

        sum += abs(sensor_data -> distance);

    }

    oi_setWheels(0,0);
    return sum;
}

double moveBump(oi_t*sensor_data, double distance){

    double totalDist = 0;

    totalDist += move_forward(sensor_data, distance);

    while (totalDist < distance){

        double diff = distance - totalDist;

        if (sensor_data->bumpLeft) {
            totalDist -= move_backward(sensor_data, 200);
            turn_right(sensor_data, 45);
            totalDist += moveBump(sensor_data, 100);
            turn_left(sensor_data, 45);

        } else if (sensor_data->bumpRight){
            totalDist -= move_backward(sensor_data, 200);
            turn_left(sensor_data, 45);
            totalDist += moveBump(sensor_data, 100);
            turn_right(sensor_data, 45);
        }

        totalDist += moveBump(sensor_data, diff);
    }
    return totalDist;

}


