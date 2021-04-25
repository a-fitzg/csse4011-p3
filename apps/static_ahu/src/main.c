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
#include "hal_hci.h"
#include "hal_packet.h"
#include <usb/usb_device.h>

void main(void) {
    
	// memcpy(tx_buffer, data, sizeof(tx_buffer));
	const struct device *usb;

    usb = device_get_binding(CONFIG_UART_CONSOLE_ON_DEV_NAME);
	
    if (usb == NULL) {
        return;
    }

    //log_init();
    if (usb_enable(NULL)) {
        return;
    }

    hal_hci_master_init();    
    k_msleep(100);

	while(1) {
        hal_parse_spi(6,0,1);// transmit request , data dont care
        k_msleep(30); // wait for spi response
        uint8_t unparsed_msg[SPI_BUFFER];
        struct UsPacket u_sensor;
        hal_hci_receive(); 
        memcpy(unparsed_msg, rxBuffer, sizeof(uint8_t) * SPI_BUFFER );
        u_sensor = hal_unparse_spi(unparsed_msg);

        if (u_sensor.type == 2 && u_sensor.preamb == 0xAA) { // check for SPI preamb and response type, then transfer sensor pulse time over BT
            uint16_t test = ((uint16_t)u_sensor.data[0] << 8) + u_sensor.data[1];
            printk("Test: %d\r\n", test);
        }

        k_msleep(30);
    }
}