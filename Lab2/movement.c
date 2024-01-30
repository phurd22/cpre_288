
#include "open_interface.h"
#include "lcd.h"

void turn_right(oi_t*sensor, double degrees){

    double sum = 0;

    oi_setWheels(-50, 50);

    while (sum < degrees-23){

        oi_update(sensor);

        sum += abs(sensor -> angle);

        lcd_printf("Angle: %3.1f", sum);

    }

    oi_setWheels(0, 0);
}


void turn_left(oi_t*sensor, double degrees){
    double sum = 0;

    oi_setWheels(50, -50);

    while (sum < degrees-23){
        oi_update(sensor);

        sum += abs(sensor -> angle);

        lcd_printf("Angle: %3.1f", sum);

       }

       oi_setWheels(0, 0);
}

double move_forward(oi_t*sensor_data, double distance_mm){

    double sum = 0;

    oi_setWheels(250, 250);

        while (sum < distance_mm) {

            oi_update(sensor_data);

            if ((sensor_data -> bumpLeft) || (sensor_data -> bumpRight)){
                oi_setWheels(0,0);
                return sum;
            }

            sum += sensor_data -> distance;

            lcd_printf("Forwards: %5.1f mm", sum);
        }

    oi_setWheels(0,0);
    return sum;
}

double move_backward(oi_t*sensor_data, double distance_mm){

    double sum = 0;

    oi_setWheels(-250,-250);

    while (sum < distance_mm) {
        oi_update(sensor_data);

        sum += abs(sensor_data -> distance);

        lcd_printf("Backwards: %5.1f mm", sum);
    }

    oi_setWheels(0,0);
    return sum;
}



