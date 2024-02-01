//Add include statements during lab
#include "open_interface.h"
#include "cyBot_uart.h"
#include "lcd.h"
#include "string.h"
#include "movement.h"

int main (void) {
    oi_t *sensor_data = oi_alloc();

    oi_init(sensor_data);

    lcd_init();

    lcd_printf("Start");

    cyBot_uart_init();

    while(1){
        char character = (char) cyBot_getByte();

        if (character == 'w'){
            move_forward(sensor_data, 250);
        }
        else if (character == 's'){
            move_backward(sensor_data, 250);
        }
        else if (character == 'a'){
            turn_left(sensor_data, 90);
        }
        else if (character == 'd'){
            turn_right(sensor_data, 90);
        }
    }

    oi_free(sensor_data);

	return 0;
}
