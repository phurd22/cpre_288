#include "open_interface.h"
#include "movement.h"
#include "lcd.h"
#include "timer.h"
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <inc/tm4c123gh6pm.h>
#include <uart-interrupt.h>

double move_forward(oi_t *self, double distance_mm)
{

    oi_setWheels(200, 200);
    double sum = 0;
    char string[20];

    while (sum < distance_mm)
    {
        oi_update(self);
        sum += self->distance;

        if (self->bumpRight || self->bumpLeft)
        {
            oi_setWheels(0, 0);
            sprintf(string, "BUMP");
            uart_sendStr(string);
            return sum;
        }
        else if (self->cliffLeft)
        {
            oi_setWheels(0, 0);
            sprintf(string, "CLIFF LEFT\r\n");
            uart_sendStr(string);
            return sum;
        }
        else if (self->cliffRight)
        {
            oi_setWheels(0, 0);
            sprintf(string, "CLIFF RIGHT\r\n");
            uart_sendStr(string);
            return sum;
        }
        else if (self->cliffFrontLeft)
        {
            oi_setWheels(0, 0);
            sprintf(string, "CLIFF FRONT LEFT\r\n");
            uart_sendStr(string);
            return sum;
        }
        else if (self->cliffFrontRight)
        {
            oi_setWheels(0, 0);
            sprintf(string, "CLIFF FRONT RIGHT\r\n");
            uart_sendStr(string);
            return sum;
        }
        else if (self->cliffLeftSignal > 2700)
        {
            oi_setWheels(0, 0);
            sprintf(string, "BORDER LEFT\r\n");
            uart_sendStr(string);
            return sum;
        }
        else if (self->cliffRightSignal > 2700)
        {
            oi_setWheels(0, 0);
            sprintf(string, "BORDER RIGHT\r\n");
            uart_sendStr(string);
            return sum;
        }
        else if (self->cliffFrontLeftSignal > 2700)
        {
            oi_setWheels(0, 0);
            sprintf(string, "BORDER FRONT LEFT\r\n");
            uart_sendStr(string);
            return sum;
        }
        else if (self->cliffFrontRightSignal > 2700)
        {
            oi_setWheels(0, 0);
            sprintf(string, "BORDER FRONT RIGHT\r\n");
            uart_sendStr(string);
            return sum;
        }
    }

    oi_setWheels(0, 0);
    return sum;
}

double move_backward(oi_t *self, double distance_mm)
{
    oi_setWheels(-200, -200);
    double sum = 0;

    while (sum < distance_mm)
    {
        oi_update(self);
        sum += abs(self->distance);

    }
    oi_setWheels(0, 0);

    return sum;
}

double turn_right(oi_t *self, double angle_deg)
{
    oi_setWheels(-100, 100);
    double sum = 0;

    while (sum < angle_deg)
    {
        oi_update(self);
        sum += abs(self->angle);
    }
    oi_setWheels(0, 0);

    return sum;
}

double turn_left(oi_t *self, double angle_deg)
{
    oi_setWheels(100, -100);
    double sum = 0;

    while (sum < angle_deg)
    {
        oi_update(self);
        sum += abs(self->angle);
    }
    oi_setWheels(0, 0);

    return sum;
}

