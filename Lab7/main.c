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


int main (void) {

    cyBOT_Scan_t getScan;

    oi_t *sensor_data = oi_alloc();

    oi_init(sensor_data);

    timer_init();

    lcd_init();

    lcd_printf("Start");

    uart_interrupt_init();

    cyBOT_init_Scan(0b0111);

    right_calibration_value = 269500;
    left_calibration_value = 1303750;

    int first = 1;

    while (1)
    {
        char character = ' ';

        if(first){
            character = (char) uart_receive();
        }
        else{
            character = 'm';
        }

        if (character == 'm'){
            char message[] = "Degrees\tIR Distance (cm)\r\n";

            uart_sendStr(message);

            cyBOT_Scan(0, &getScan);

            timer_waitMillis(300);

            int i, k = 0;
            int raw;
            int rawNum;
            int distances[91];
            for(i = 0; i <= 180; i += 2)
            {
                cyBOT_Scan(i, &getScan);
                raw = getScan.IR_raw_val;

                distances[k] = 534.761271*exp(-.00325036788*raw)+ 8.91103269;

                char data[80];
                sprintf(data, "%d\t%d\r\n", i,  distances[k]);

                uart_sendStr(data);

                k++;
            }

            lcd_printf("Finished scanning");
            int isObject = 0;
            int objectNumber = 0; 
            int startAngle = 0;
            int endAngle = 0, midAngle = 0, smallestObjectAngle = 90;
            double distance = 0, width = 0, smallestDist = 0, smallestWidth = 0;
            double prevWidth = 100000;

            for(i=2; i<90; i++){
                //detected an object
                if (distances[i] < 35) {
                    //detecting new object
                    if ((distances[i-1] > 35) && (distances[i-2] > 35)) {
                        objectNumber++;
                        startAngle = i*2;
                    //updating end angle if the object is still there
                    } else {
                        endAngle = i*2;
                    }
                } else {
                    //do calculationsg
                    if ((distances[i-1] < 35) && (distances[i-2] < 35))
                    {
                        isObject = 1;
                        midAngle = (startAngle+endAngle)/2;
                        if ((midAngle%2) != 0) {
                            midAngle = midAngle+1;
                        }

                        cyBOT_Scan(midAngle, &getScan);
                        timer_waitMillis(300);
                        cyBOT_Scan(midAngle, &getScan);
                        distance = getScan.sound_dist;
                        width = 2*3.14159*distance*((endAngle - startAngle) / 360.0);


                        char data[80];
                        sprintf(data, "%d\t%d\t%f\t%f\r\n", objectNumber, midAngle, distance, width);

                        uart_sendStr(data);

                        if (width <= prevWidth) {
                            smallestObjectAngle = midAngle;
                            smallestDist = distance;
                            smallestWidth = width;
                        }
                        prevWidth = width;
                    }
                }
            }

            if (isObject) {
             //position sensor to smallest object
                 cyBOT_Scan(smallestObjectAngle, &getScan);

                 //move to smallest object
                 //turn bot
                 if (smallestObjectAngle < 90){
                     //turn right
                     turn_right(sensor_data, 90-smallestObjectAngle - 5);
                 } else {
                     //turn left
                     turn_left(sensor_data, smallestObjectAngle-90 - 5);
                 }
                 //move forwards dist
                 double reqDistance = (smallestDist*10) - 75;
                 first = 0;
                 lcd_printf("%.2f", moveBump(sensor_data, reqDistance));
                 first = 1;


             } else {
                 lcd_printf("No objects in view\n%.2f", moveBump(sensor_data, 500));
                 objectNumber = 0;
                 prevWidth = 0;
                 smallestObjectAngle = 90;
                 distance = 0;
                 first = 0;
                 isObject = 0;
             }



        }

    }
    oi_free(sensor_data);


    return 0;
}
