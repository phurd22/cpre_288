/**
 * Driver for ping sensor
 * @file ping.c
 * @author
 */

#include "ping.h"
#include "Timer.h"

volatile unsigned long START_TIME = 0;
volatile unsigned long END_TIME = 0;
volatile enum{LOW, HIGH, DONE} STATE = LOW; // State of ping echo pulse
#define MICROS_PER_TICK 64999UL // Number of microseconds in one timer cycle

void ping_init (void){

  // YOUR CODE HERE
    SYSCTL_RCGCGPIO_R |= 0b000010;
    while ((SYSCTL_PRGPIO_R & 0x02) == 0) {};
    GPIO_PORTB_DEN_R |= 0x08;
    GPIO_PORTB_DIR_R &= ~0x08;
    GPIO_PORTB_AFSEL_R |= 0x08;
    GPIO_PORTB_PCTL_R &= 0x00000000;     // Force 0's in the desired locations
    GPIO_PORTB_PCTL_R |= 0x00007000;     // Force 1's in the desired locations


   SYSCTL_RCGCTIMER_R |= SYSCTL_RCGCTIMER_R3; // Turn on clock to TIMER3
   TIMER3_CTL_R &= ~TIMER_CTL_TBEN;           // Disable TIMER3 for setup
   TIMER3_CFG_R = TIMER_CFG_16_BIT;           // Set as 16-bit timer
   TIMER3_TBMR_R = TIMER_TBMR_TBMR_PERIOD;    // Periodic, countdown mode
   TIMER3_TBILR_R = MICROS_PER_TICK - 1;      // Countdown time of 65ms
   TIMER3_ICR_R |= TIMER_ICR_TBTOCINT; // Clear timeout interrupt status
   TIMER3_TBPR_R = 0x0F;               // 15 gives a period of 1us
   TIMER3_IMR_R |= TIMER_IMR_TBTOIM;   // Allow TIMER3 timeout interrupts
   NVIC_PRI23_R |= NVIC_PRI23_INTB_M;  // Priority 7 (lowest)
   NVIC_EN2_R |= (1 << 28);

    IntRegister(INT_TIMER3B, TIMER3B_Handler);

    IntMasterEnable();

    // Configure and enable the timer
    TIMER3_CTL_R |= 0x0C00;
}

void ping_trigger (void){
    STATE = LOW;
    // Disable timer and disable timer interrupt
    TIMER3_CTL_R &= ~TIMER_CTL_TBEN;
    TIMER3_IMR_R &= ~TIMER_IMR_TBTOIM;
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

    GPIO_PORTB_DIR_R &= ~0x08;
    // Clear an interrupt that may have been erroneously triggered
    TIMER3_ICR_R |= TIMER_ICR_TBTOCINT;
    // Re-enable alternate function, timer interrupt, and timer
    GPIO_PORTB_AFSEL_R |= 0x08;
    TIMER3_IMR_R |= TIMER_IMR_TBTOIM;
    TIMER3_CTL_R |= TIMER_CTL_TBEN;


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

}

float ping_getDistance (void){

    // YOUR CODE HERE

}
