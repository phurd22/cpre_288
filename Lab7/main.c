//Add include statements during lab
#include "Timer.h"
#include "lcd.h"
#include "uart-interrupt.h"
#include "cyBot_Scan.h"
#include "open_interface.h"
#include "string.h"
#include <stdio.h>
#include "movement.h"
#include <math.h>


int main (void) {

    cyBOT_Scan_t getScan;

    timer_init();

    lcd_init();

    lcd_printf("Start");

    uart_interrupt_init();

    cyBOT_init_Scan(0b0111);

    right_calibration_value =  243250;
    left_calibration_value = 1230250;

    oi_t *sensor_data = oi_alloc();

    oi_init(sensor_data);

    while (1)
    {
        char character = (char) uart_receive();
        int objectNumber = 0;
        double distances[90];
        int startAngle;
        int endAngle;
        int midAngle;
        double distance;
        int radWidth;
        int prevRadWidth = 200;
        int smallestObjectAngle;
        int smallestDist;

        if (character == 'm'){
            char message[] = "Degrees\tIR Distance (cm)\r\n";

            uart_sendStr(message);

            cyBOT_Scan(0, &getScan);

            timer_waitMillis(300);

            int i, k = 0, p;
            int raw[91];
            int rawNum;
            int distance[91];
            for(i = 0; i < 180; i += 2)
            {
                rawNum = 0;
                for (p = 0; p < 3; ++p) {
                    cyBOT_Scan(i, &getScan);
                    rawNum += getScan.IR_raw_val;
                }
                raw[k] = (int) (rawNum/3);
                distance[k] = ((1.13307625*pow(10,3))*(exp(-0.00323623677*raw[k])))+12.7014549;

                char data[80];
                sprintf(data, "%d\t%d\r\n", i,  distance[k]);

                uart_sendStr(data);

                k++;
            }

            lcd_printf("Finished scanning");

//            for(i=2; i<90; i++){
//                //detected an object
//                if (distances[i] < 100) {
//                    //detecting new object
//                    if ((distances[i-1] > 100) && (distances[i-2] > 100)) {
//                        objectNumber++;
//                        startAngle = i*2;
//                    //updating end angle if the object is still there
//                    } else {
//                        endAngle = i*2;
//                    }
//                } else {
//                    //do calculations
//                    if ((distances[i-1] < 100) && (distances[i-2] < 100))
//                    {
//                        midAngle = (startAngle+endAngle)/2;
//                        if ((midAngle%2) != 0) {
//                            midAngle = midAngle+1;
//                        }
//                        distance = distances[midAngle/2];
//                        radWidth = endAngle - startAngle;
//
//                        char data[80];
//                        sprintf(data, "%d\t%d\t%f\t%d\r\n", objectNumber, midAngle, distance, radWidth);
//
//                        int g = 0;
//                        for(g = 0; g < strlen(data); g++){
//                            cyBot_sendByte(data[g]);
//                       }
//
//                        if (radWidth < prevRadWidth) {
//                            smallestObjectAngle = midAngle;
//                            smallestDist = distance;
//                        }
//                        prevRadWidth = radWidth;
//                    }
//                }
//            }

//            //position sensor to smallest object
//            cyBOT_Scan(smallestObjectAngle, &getScan);
//
//            //move to smallest object
//            //turn bot
//            if (smallestObjectAngle < 90){
//                //turn right
//                turn_right(sensor_data, 90-smallestObjectAngle);
//            } else {
//                //turn left
//                turn_left(sensor_data, smallestObjectAngle-90);
//            }
//            //move forwards dist
//            move_forward(sensor_data, (smallestDist*10)-100);
//
        }

    }
    oi_free(sensor_data);


    return 0;
}
