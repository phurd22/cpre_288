//Add include statements during lab
#include "open_interface.h"
#include "movement.h"
#include "lcd.h"
#include "cyBot_Scan.h"
#include "cyBot_uart.h"

int main (void) {
    timer_init();
    lcd_init();
    cyBOT_init_Scan(0b0111);
    cyBOT_SERVO_cal();
//    right_calibration_value =  306250; //232750;
//    left_calibration_value = 1293250; //1225000;
//
//    int i;
//    cyBOT_Scan_t scan;
//    for(i=0; i<=180; i+=2){
//        cyBOT_Scan(i, &scan);
//    }

	return 0;
}
