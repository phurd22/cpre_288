//Add include statements during lab
#include "open_interface.h"

int main (void) {

	oi_t *sensor_data = oi_alloc();

    oi_init(sensor_data);


	return 0;
}