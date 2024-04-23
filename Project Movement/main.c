/// Simple 'Hello, world' program
/**
 * This program prints "Hello, world" to the LCD screen
 * @author Chad Nelson
 * @date 06/26/2012
 *
 * updated: phjones 9/3/2019
 * Description: Added timer_init call, and including Timer.h
 */

#include "Timer.h"
#include "lcd.h"
#include <string.h>
#include <stdint.h>
#include "movement.h"
#include "open_interface.h"
#include "stdio.h"
#include "uart-interrupt.h"

int main (void) {

    timer_init();
    uart_interrupt_init();

	oi_t *sensor_data = oi_alloc(); //allocates memory
	oi_init(sensor_data); //initializes sensors

	int first = 1;

	while(1) {

        char character = ' ';

        if (first == 1)
        {
            character = (char) uart_receive();
        }
        else
        {
            character = 'm';
        }

	    if (character == 'm') {
	        move_forward(sensor_data, 1000);
	    }
   }

	oi_free(sensor_data);

	return 0;
}
