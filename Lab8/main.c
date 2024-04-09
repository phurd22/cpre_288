//Add include statements during lab
#include "Timer.h"
#include "lcd.h"
#include "uart-interrupt.h"
#include "open_interface.h"
#include "cyBot_Scan.h"
#include "string.h"
#include <stdio.h>
#include "movement.h"
#include <math.h>
#include "adc.h"


int main (void) {
    adc_init();
    timer_init();
    lcd_init();
    lcd_printf("Start");

    while(1) {
        uint16_t result = adc_read();
        double dist = 534.761271*exp(-.00325036788*result)+ 8.91103269;
        lcd_printf("%d, %.2f", result, dist);
        timer_waitMillis(2000);
    }

}
