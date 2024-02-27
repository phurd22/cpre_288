//Add include statements during lab
#include "lcd.h"
#include "cyBot_uart.h"
#include "cyBot_Scan.h"
#include "string.h"
#include <stdio.h>

int main (void) {

    cyBOT_Scan_t getScan;

    lcd_init();

    lcd_printf("Start");

    cyBot_uart_init();

    cyBOT_init_Scan(0b0111);

    right_calibration_value =  232750;
    left_calibration_value = 1225000;

    timer_init();

    while (1)
    {
        char character = (char) cyBot_getByte();

        if (character == 'm'){

            char message[] = "Degrees\tPING Distance (cm)\r\n";
            int i;
            for(i = 0; i < strlen(message); i++){
               cyBot_sendByte(message[i]);
            }

            for(i = 45; i < 137; i += 2)
            {
                cyBOT_Scan(i, &getScan);
                char data[80];
                sprintf(data, "%d\t%f\r\n", i, getScan.sound_dist);

                int j = 0;
                for(j = 0; j < strlen(data); j++){
                    cyBot_sendByte(data[j]);
               }
            }
        }
    }


	return 0;
}
