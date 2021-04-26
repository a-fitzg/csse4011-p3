#include <zephyr.h>
#include <sys/printk.h>
#include <device.h>
#include <devicetree.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <drivers/gpio.h>
#include <sys_clock.h>
#include <sys/util.h>
#include <limits.h>
#include "hal_ultrasonic.h"
#include "hal_hci.h"
#include "hal_packet.h"

void main() {
    hal_hci_slave_init();
    hal_ultrasonic_init();
    uint16_t pulse_reading;
    uint8_t data[2];
    uint8_t unparsed_msg[SPI_BUFFER];
    struct UsPacket u_sensor;
    uint8_t* parsed_msg;
    while(1) {
        struct UsPacket u_sensor;
        hal_hci_receive(); 
        memcpy(unparsed_msg, rxBuffer, sizeof(uint8_t) * SPI_BUFFER );
        u_sensor = hal_unparse_spi(unparsed_msg);
        if (u_sensor.type == 1 && u_sensor.sid == 6) { // request
            pulse_reading = hal_ultrasonic_read();
            data[0] = pulse_reading >> 8;// upper 8 bit data
            data[1] = pulse_reading & 0xFF; // lower 8 bit data
            // printf("test pulse reading: %d\r\n", pulse_reading);
            hal_parse_spi(6, pulse_reading, 2);
            // uint16_t test = ((uint16_t)data[0] << 8) + data[1];
            // printf("test convert: %d\r\n", test);
            // printf("Preamb: %d  Type: %d  SID: %d  Value:  %d\r\n", *(parsed_msg + 0), *(parsed_msg + 1), *(parsed_msg + 3), test);
            //k_msleep(200);
        }
    }
}
