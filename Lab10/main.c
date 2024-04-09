/**
 * @file lab9_template.c
 * @author
 * Template file for CprE 288 Lab 9
 */

#include "Timer.h"
#include "lcd.h"
#include "servo.h"


int main(void) {
	timer_init(); // Must be called before lcd_init(), which uses timer functions
	lcd_init();
	servo_init();

	// YOUR CODE HERE
	//servo_in();

	servo_move(0);
	timer_waitMillis(2000);
	servo_move(90);
	timer_waitMillis(2000);
	servo_move(180);



}
