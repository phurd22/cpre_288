#include <stdint.h>
#include <stdbool.h>
#include <inc/tm4c123gh6pm.h>
#include "Timer.h"


void servo_init(){
    SYSCTL_RCGCGPIO_R |= 0b000010;
    while ((SYSCTL_PRGPIO_R & 0x02) == 0) {};
    GPIO_PORTB_DEN_R |= 0x20;
    GPIO_PORTB_DIR_R &= ~0x20;
    GPIO_PORTB_AFSEL_R |= 0x20;
    GPIO_PORTB_PCTL_R &= ~0x00700000;     // Force 0's in the desired locations
    GPIO_PORTB_PCTL_R |= 0x00700000;     // Force 1's in the desired locations

    SYSCTL_RCGCTIMER_R |= 0x02;                  // Turn on clock to TIMER1 //
    while (SYSCTL_RCGCTIMER_R & 0x02 == 0) {};   //running the clock
    TIMER1_CTL_R &= ~0x100;                      // Disable TIMER1 for setup
    TIMER1_CFG_R = 0x00000004;                         // Set as 16-bit timer
    TIMER1_TBMR_R |= 0x0A;
    TIMER1_TBMR_R &= ~0x04;
    //TIMER1_TBMR_R |= 0x02;
    TIMER1_CTL_R &= ~0x4000;
    TIMER1_TBPR_R = 0x04;
    TIMER1_TBILR_R = 0x4E200; //value needs to be 20ms in clock cycles
    TIMER1_TBMATCHR_R = 0x8440;//0x1731;  //value needs to be 20 - 1.5 in clock cycles to set in to 90
    TIMER1_TBPMR_R = 0x04; //0x00;  //overflow of the match value into the prescaler
    TIMER1_CTL_R |= 0x100;
}

void servo_move(uint16_t degrees){
    uint16_t high_time_ms = (degrees/180)-1;
    uint16_t low_time_ms = 20-high_time_ms;

    int decimal = 320000 - 8000 - ((28000*degrees)/180);
    //checkpoint
    TIMER1_TBMATCHR_R = decimal & 0xFFFF;  //value needs to be 20 - 1.5 in clock cycles to set in to 90
    TIMER1_TBPMR_R = decimal >> 16;
    timer_waitMillis(5);
}
