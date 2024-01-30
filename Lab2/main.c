//Add include statements during lab
#include "open_interface.h"
#include "movement.h"
#include "lcd.h"

int main (void) {
    double totalDistance = 0;
	oi_t *sensor_data = oi_alloc();

    oi_init(sensor_data);

    lcd_init();

    lcd_printf("Start");

    while (totalDistance < 2000){

        totalDistance += move_forward(sensor_data, 2000-totalDistance);

        if (totalDistance < 2000) {

            if (sensor_data->bumpLeft) {
                totalDistance -= move_backward(sensor_data, 150);
                turn_right(sensor_data, 90);
                move_forward(sensor_data, 250);
                turn_left(sensor_data, 90);

            } else if (sensor_data->bumpRight){
                totalDistance -= move_backward(sensor_data, 150);
                turn_left(sensor_data, 90);
                move_forward(sensor_data, 250);
                turn_right(sensor_data, 90);
            }
        }
        lcd_printf("Total: %5.1f mm", totalDistance);
    }

    oi_free(sensor_data);

	return 0;
}
