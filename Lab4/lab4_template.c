/**
 * lab4_template.c
 *
 * Template file for CprE 288 lab 4
 *
 * @author Zhao Zhang, Chad Nelson, Zachary Glanz
 * @date 08/14/2016
 */

#include "button.h"
#include "Timer.h"
#include "lcd.h"
#include "cyBot_uart.h"
#include "putty_message.h"
#include "string.h" // Functions for communicating between CyBot and Putty (via UART)
                         // PuTTy: Baud=115200, 8 data bits, No Flow Control, No Parity, COM1


int main(void) {
	button_init();
	timer_init();
	lcd_init();
	cyBot_uart_init();
	int prevButton = 0;

	 while(1) {
	       int button = button_getButton();

	       if ((button == 1) && (prevButton != 1)) {
	           putty_message("Self Destruction\r\n");
	       }
	       else if ((button == 2) && (prevButton != 2)) {
	           putty_message("Sending noodles\r\n");
	       }
	       else if ((button == 3) && (prevButton != 3)) {
	           putty_message("Peter is very smart for a large dog\r\n");
	       }
	       else if ((button == 4) && (prevButton != 4)) {
	           putty_message("Sarah much smarter than Peter\r\n");
	       }

	       prevButton = button;
	 }
}
