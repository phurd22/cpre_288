//Add include statements during lab
#include "open_interface.h"
#include "movement.h"
#include "lcd.h"
#include "cyBot_Scan.h"
#include "uart-interrupt.h"

int main (void) {
    timer_init();
    lcd_init();
    cyBOT_init_Scan(0b0111);
    right_calibration_value =  243250;
    left_calibration_value = 1230250;
    cyBOT_Scan_t getScan;
    uart_interrupt_init();

    cyBOT_Scan(90, &getScan);

    while (1) {
        char character = (char) uart_receive();

        if (character == 'm'){
            cyBOT_Scan(90, &getScan);

            char data[80];
            sprintf(data, "%d\r\n", getScan.IR_raw_val);
            //distances[k] = getScan.IR_raw_val;

            uart_sendStr(data);
        }
    }


	return 0;
}
