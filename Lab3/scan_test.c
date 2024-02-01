//Add include statements during lab
#include "lcd.h"
#include "cyBot_uart.h"
#include "cyBot_Scan.h"
#include "string.h"

int main (void) {

    cyBOT_Scan_t *getScan;

    lcd_init();

    lcd_printf("Start");

    cyBot_uart_init();

    cyBOT_init_Scan(0b0111);

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


            for(i = 45; i < 138; i += 3)
            {
                cyBOT_Scan(i, getScan);
                char data[10];
                strcat(data, i);
                strcat(data, '\t');
                strcat(data, (char) getScan -> sound_dist);
                strcat(data, '\r\n');

                for(i = 0; i < strlen(data); i++){
                    cyBot_sendByte(data[i]);
                 }
                timer_waitMillis(300);
            }
        }
    }


	return 0;
}
