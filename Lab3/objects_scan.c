//Add include statements during lab
#include "Timer.h"
#include "lcd.h"
#include "cyBot_uart.h"
#include "cyBot_Scan.h"
#include "open_interface.h"
#include "string.h"
#include <stdio.h>
#include "movement.h"


int main (void) {

    cyBOT_Scan_t getScan;

    timer_init();

    lcd_init();

    lcd_printf("Start");

    cyBot_uart_init();

    cyBOT_init_Scan(0b0111);

    right_calibration_value =  295750; //232750;
    left_calibration_value = 1230250; //1225000;

    oi_t *sensor_data = oi_alloc();

    oi_init(sensor_data);




    while (1)
    {
        char character = (char) cyBot_getByte();
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

            char message[] = "Degrees\tPING Distance (cm)\r\n";
            int i;
            for(i = 0; i < strlen(message); i++){
               cyBot_sendByte(message[i]);
            }
            int k = 0;
            cyBOT_Scan(0, &getScan);

            timer_waitMillis(300);

            for(i = 0; i < 180; i += 2)
            {
                cyBOT_Scan(i, &getScan);
                char data[80];
                sprintf(data, "%d\t%f\r\n", i, getScan.sound_dist);
                distances[k] = getScan.sound_dist;

                int j = 0;
                for(j = 0; j < strlen(data); j++){
                    cyBot_sendByte(data[j]);
                }
                k++;
            }

            lcd_printf("Finished scanning");

            for(i=2; i<90; i++){
                //detected an object
                if (distances[i] < 100) {
                    //detecting new object
                    if ((distances[i-1] > 100) && (distances[i-2] > 100)) {
                        objectNumber++;
                        startAngle = i*2;
                    //updating end angle if the object is still there
                    } else {
                        endAngle = i*2;
                    }
                } else {
                    //do calculations
                    if ((distances[i-1] < 100) && (distances[i-2] < 100))
                    {
                        midAngle = (startAngle+endAngle)/2;
                        if ((midAngle%2) != 0) {
                            midAngle = midAngle+1;
                        }
                        distance = distances[midAngle/2];
                        radWidth = endAngle - startAngle;

                        char data[80];
                        sprintf(data, "%d\t%d\t%f\t%d\r\n", objectNumber, midAngle, distance, radWidth);

                        int g = 0;
                        for(g = 0; g < strlen(data); g++){
                            cyBot_sendByte(data[g]);
                       }

                        if (radWidth < prevRadWidth) {
                            smallestObjectAngle = midAngle;
                            smallestDist = distance;
                        }
                        prevRadWidth = radWidth;
                    }
                }
            }

            //position sensor to smallest object
            cyBOT_Scan(smallestObjectAngle, &getScan);

            //move to smallest object
            //turn bot
            if (smallestObjectAngle < 90){
                //turn right
                turn_right(sensor_data, 90-smallestObjectAngle);
            } else {
                //turn left
                turn_left(sensor_data, smallestObjectAngle-90);
            }
            //move forwards dist
            move_forward(sensor_data, (smallestDist*10)-100);

        }

    }
    oi_free(sensor_data);


	return 0;
}
