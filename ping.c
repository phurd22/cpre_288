/**
 * Driver for ping sensor
 * @file ping.c
 * @author
 */

#include "ping.h"
#include "Timer.h"

volatile unsigned long START_TIME = 0;
volatile unsigned long END_TIME = 0;
int overflow = 0;
volatile enum{LOW, HIGH, DONE} STATE = LOW; // State of ping echo pulse
#define MICROS_PER_TICK 64999UL // Number of microseconds in one timer cycle

void ping_init (void){

  // YOUR CODE HERE
    SYSCTL_RCGCGPIO_R |= 0b000010;
    while ((SYSCTL_PRGPIO_R & 0x02) == 0) {};
    GPIO_PORTB_DEN_R |= 0x08;
    GPIO_PORTB_DIR_R &= ~0x08;
    GPIO_PORTB_AFSEL_R |= 0x08;
    GPIO_PORTB_PCTL_R &= 0xFFFF0FFF;     // Force 0's in the desired locations
    GPIO_PORTB_PCTL_R |= 0x00007000;     // Force 1's in the desired locations


   SYSCTL_RCGCTIMER_R |= 0x08;                  // Turn on clock to TIMER3 //
   while (SYSCTL_RCGCTIMER_R & 0x08 == 0) {};   //running the clock
   TIMER3_CTL_R &= ~0x100;                      // Disable TIMER3 for setup
   TIMER3_CFG_R = 0x04;                         // Set as 16-bit timer
   TIMER3_TBMR_R |= 0x07;
   TIMER3_TBMR_R &= ~0x10;                       // Periodic, countdown mode
   TIMER3_TBILR_R |= 0xFFFF;      // Countdown time of 65ms
   TIMER3_ICR_R |= 0x400;      // Clear flag
   TIMER3_TBPR_R = 0xFF;                     // 15 gives a period of 1us
   TIMER3_IMR_R |= 0x400;         // Allow TIMER3 timeout interrupts

   NVIC_EN1_R |= 0x10;
   NVIC_PRI9_R |= 0x20;

    IntRegister(INT_TIMER3B, TIMER3B_Handler);

    IntMasterEnable();

    // Configure and enable the timer
    TIMER3_CTL_R |= 0x0C00; //configure
    TIMER3_CTL_R |= 0x0100; //enable
}

void ping_trigger (void){
    STATE = LOW;
    // Disable timer and disable timer interrupt
    TIMER3_CTL_R &= ~0x100;
    TIMER3_IMR_R &= ~0x400;
    // Disable alternate function (disconnect timer from port pin)
    GPIO_PORTB_DIR_R |= 0x08;
    GPIO_PORTB_AFSEL_R &= ~0x08;

    // YOUR CODE HERE FOR PING TRIGGER/START PULSE
    GPIO_PORTB_DATA_R &= ~0x08;
    GPIO_PORTB_DATA_R |= 0x08;
    STATE = HIGH;
    timer_waitMicros(10); //waits for 10 us
    GPIO_PORTB_DATA_R &= ~0x08;
    STATE = DONE;

    // Clear an interrupt that may have been erroneously triggered
    TIMER3_ICR_R |= 0x400;
    // Re-enable alternate function, timer interrupt, and timer
    GPIO_PORTB_AFSEL_R |= 0x08;
    TIMER3_IMR_R |= 0x400;
    TIMER3_CTL_R |= 0x100;

}

void TIMER3B_Handler(void){

  // YOUR CODE HERE
  // As needed, go back to review your interrupt handler code for the UART lab.
  // What are the first lines of code in the ISR? Regardless of the device, interrupt handling
  // includes checking the source of the interrupt and clearing the interrupt status bit.
  // Checking the source: test the MIS bit in the MIS register (is the ISR executing
  // because the input capture event happened and interrupts were enabled for that event?
  // Clearing the interrupt: set the ICR bit (so that same event doesn't trigger another interrupt)
  // The rest of the code in the ISR depends on actions needed when the event happens.

    //clearing interrupt status
    //TIMER3_MIS_R |= 0x400;
    //TIMER3_ICR_R |= 0x400;

    //long timeStart, timeEnd;

    //Checking the source: test the MIS bit in the MIS register (is the ISR executing
    if (TIMER3_MIS_R &= 0x400) {
        //Clearing the interrupt: set the ICR bit
        TIMER3_ICR_R |= 0x400;

        if(STATE == LOW){
            START_TIME = TIMER3_TBR_R; //gets start time in micros
            STATE = HIGH;
        }
        else if(STATE == HIGH){
            END_TIME = TIMER3_TBR_R; //gets end time in micros
            STATE = DONE;
        }
    }

}

float ping_getDistance (void){

    // YOUR CODE HERE
    ping_trigger();
    while(STATE != DONE);
    STATE = LOW;
    float dist = 0;

    if (END_TIME > START_TIME){
        overflow++;
        dist = (START_TIME - END_TIME + 0xFFFFFF) * 0.5 * 343 * 0.000006;
    }
    else {
        dist = (START_TIME - END_TIME) * 0.5 * 343 * 0.000006;
    }
    return dist;
}
