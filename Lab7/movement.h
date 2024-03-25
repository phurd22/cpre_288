#ifndef MOVEMENT_H

#define MOVEMENT_H

//Function headers and macro definitions
double move_forward(oi_t*sensor_data, double distance_mm);

double move_backward(oi_t*sensor_data, double distance_mm);

void turn_right(oi_t*sensor, double degrees);

void turn_left(oi_t*sensor, double degrees);

double moveBump(oi_t*sensor_data, double distance);

#endif
