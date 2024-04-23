#ifndef MOVEMENT_H_
#define MOVEMENT_H_

#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include "Timer.h"
#include <inc/tm4c123gh6pm.h>
#include "lcd.h"
#include "open_interface.h"

double move_forward(oi_t *self, double distance_mm);
double turn_right(oi_t *sensor, double degrees);
double turn_left(oi_t *sensor, double degrees);
double move_backward(oi_t *self, double distance_mm);
double cliff_detection(oi_t *sensor);

#endif
