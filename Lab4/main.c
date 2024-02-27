//Add include statements during lab
#include "open_interface.h"
#include "lcd.h"
#include "button.h"
#include "timer.h"
#include "cyBot_uart.h"

int main (void) {
   timer_init();
   lcd_init();
   button_init();

   while(1) {
       int button = button_getButton();

       lcd_printf("Button %d was pressed", button);
   }
   return 0;
}
