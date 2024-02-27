#include "open_interface.h"
#include "cyBot_uart.h"
#include "lcd.h"
#include "string.h"

void putty_message(char message[]) {
    int i = 0;

    for(i = 0; i < strlen(message); i++){
        cyBot_sendByte(message[i]);
    }
}
