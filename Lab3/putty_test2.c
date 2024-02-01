//Add include statements during lab
#include "open_interface.h"
#include "cyBot_uart.h"
#include "lcd.h"
#include "string.h"

int main (void) {

    lcd_init();

    lcd_printf("Start");

    cyBot_uart_init();

    while(1){
        char character = (char) cyBot_getByte();

        lcd_putc(character);
        
        char message[] = "Got a(n) ";

        int i = 0;

        for(i, i < strlen(message), i++){
            cyBot_sendByte(message[i])
        }

        cBot_sendByte(character)
    }

	return 0;
}
