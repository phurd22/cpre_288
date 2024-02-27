/**
 * lab6_template.c
 *
 * Template file for CprE 288 Lab 6
 *
 * @author Diane Rover, 2/15/2020
 *
 */

#include "Timer.h"
#include "lcd.h"
#include "cyBot_Scan.h"  // For scan sensors
#include "uart-interrupt.h"

// Uncomment or add any include directives that are needed
// #include "open_interface.h"
// #include "movement.h"
// #include "button.h"


#warning "Possible unimplemented functions"
#define REPLACEME 0


int main(void) {
	timer_init(); // Must be called before lcd_init(), which uses timer functions
	lcd_init();
	uart_interrupt_init();
	cyBOT_init_Scan(0b0111);

	// YOUR CODE HERE
	cyBOT_Scan_t getScan;

	while(1)
	{
	    char character = (char) uart_receive();

        if (character == 'g'){

            char message[] = "Degrees\tPING Distance (cm)\r\n";
            int i;
            for(i = 0; i < strlen(message); i++){
                uart_sendChar(message[i]);
            }

            for(i = 45; i < 137; i += 2)
            {
                if(!command_flag) {
                    cyBOT_Scan(i, &getScan);
                    char data[80];
                    sprintf(data, "%d\t%f\r\n", i, getScan.sound_dist);

                    int j = 0;
                    for(j = 0; j < strlen(data); j++){
                        uart_sendChar(data[j]);
                   }
                }
                else{
                    command_flag = 0;
                    break;
                }
            }
        }
	}

}
