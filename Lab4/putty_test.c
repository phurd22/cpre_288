//Add include statements during lab
#include "open_interface.h"
#include "cyBot_uart.h"
#include "lcd.h"

int main (void) {

    lcd_init();

    lcd_printf("Start");

    cyBot_uart_init();

    while(1){
        int message = cyBot_getByte();

        lcd_putc((char) message);

    }

	return 0;
}
