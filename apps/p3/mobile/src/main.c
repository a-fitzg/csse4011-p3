/* main.c - Application main entry point */

/*
 * Copyright (c) 2015-2016 Intel Corporation
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr.h>
#include <zephyr/types.h>
#include <device.h>
#include <devicetree.h>
#include <drivers/gpio.h>
#include <logging/log.h>
#include <stddef.h>
#include <sys/printk.h>
#include <sys/util.h>
#include <kernel.h>
#include <drivers/uart.h>
#include <usb/usb_device.h>

#include <bluetooth/bluetooth.h>
#include <bluetooth/hci.h>

#include <os_bluetooth.h>

LOG_MODULE_REGISTER(main);

// Each static node is represented by a struct, and this is a list of them
NodeListItem nodeList[NUM_STATIC_NODES];

// Mutex, to ensure that only one thread can access the Node items at once
struct k_mutex os_MutexNodeList;

// Initialise message queue (bluetooth messages from static nodes)
K_MSGQ_DEFINE(os_QueueBtNodeMessage, sizeof(NodeQueueItem), 
        BT_QUEUE_LENGTH, NODE_QUEUE_ALIGNMENT);

// Initialise thread for processing incoming messages
K_THREAD_DEFINE(os_TaskBtNodeMessage, BT_THREAD_STACK_SIZE, 
        os_bluetoothMobileListen, NULL, NULL, NULL, BT_THREAD_PRIORITY, 0, 0);

static const struct bt_data mobileResponseData[] = {                                   
    BT_DATA(BT_DATA_NAME_COMPLETE, DEVICE_NAME, DEVICE_NAME_LEN),               
}; 


void main(void) {

	struct bt_le_scan_param scan_param = {
		.type       = BT_HCI_LE_SCAN_PASSIVE,
		.options    = BT_LE_SCAN_OPT_NONE,
		.interval   = 0x0005,
		.window     = 0x0005,
	};
	int err;
    int btErr;

    device_get_binding(CONFIG_UART_CONSOLE_ON_DEV_NAME);

    if (usb_enable(NULL)) {
        return;
    }

    // Initialise node list mutex
    k_mutex_init(&os_MutexNodeList);

    // Initialise known bluetooth static nodes
    NodeListItem node1 = {.index = 0, .node = 
            {.address = {.val = {0x80, 0x17, 0xF3, 0x5A, 0x73, 0xD8}}, 
            .hasUltrasonic = 1, .rssi = -128, .ultrasonic = {0, 0}}};
    NodeListItem node2 = {.index = 1, .node = 
            {.address = {.val = {0x78, 0x8B, 0x23, 0xD3, 0x34, 0xF0}}, 
            .hasUltrasonic = 1, .rssi = -128, .ultrasonic = {0, 0}}};
    NodeListItem node3 = {.index = 2, .node = 
            {.address = {.val = {0xD2, 0x3D, 0x4E, 0x14, 0x23, 0xD9}}, 
            .hasUltrasonic = 0, .rssi = -128, .ultrasonic = {0, 0}}};
    NodeListItem node4 = {.index = 3, .node = 
            {.address = {.val = {0xAF, 0xDE, 0xCD, 0xD4, 0x38, 0xE1}}, 
            .hasUltrasonic = 0, .rssi = -128, .ultrasonic = {0, 0}}};

    nodeList[0] = node1;
    nodeList[1] = node2;
    nodeList[2] = node3;
    nodeList[3] = node4;

    k_sleep(K_MSEC(10000));

	//printk("Starting Scanner/Advertiser Demo\n");

	// Initialize the Bluetooth Subsystem
	err = bt_enable(NULL);
	if (err) {
		printk("Bluetooth init failed (err %d)\n", err);
		return;
	}

	printk("Bluetooth initialized\n");

	err = bt_le_scan_start(&scan_param, scan_cb);
	if (err) {
		printk("Starting scanning failed (err %d)\n", err);
		return;
	}

    // We have started scanning, now 
    while (1) {

        // RSSI values
        int8_t rssi0, rssi1, rssi2, rssi3;
        // Ultrasonic values
        uint8_t us0[2];
        uint8_t us1[2];
        // Timestamp
        // Sensor values

        // Now get the values
        // Accessing variable shared across multiple threads, need to ensure
        // only 1 thread access the variables at once
        k_mutex_lock(&os_MutexNodeList, K_FOREVER);

        // TODO - GET VALUES
        rssi0 = nodeList[0].node.rssi;
        rssi1 = nodeList[1].node.rssi;
        rssi2 = nodeList[2].node.rssi;
        rssi3 = nodeList[3].node.rssi;

        // Define node list items 0 and 1 ultrasonic nodes
        us0[0] = nodeList[0].node.ultrasonic[0];
        us0[1] = nodeList[0].node.ultrasonic[1];
        us1[0] = nodeList[1].node.ultrasonic[0];
        us1[1] = nodeList[1].node.ultrasonic[1];

        uint32_t uptime = (uint32_t)k_uptime_get();

        k_mutex_unlock(&os_MutexNodeList);

        union {
            uint32_t        time;
            unsigned char   bytes[4];
        } timeConverter ;
        
        timeConverter.time = uptime;

        btErr = bt_le_adv_stop();

        const struct bt_data tempAd[] = {
                BT_DATA_BYTES(BT_DATA_FLAGS, (BT_LE_AD_GENERAL | BT_LE_AD_NO_BREDR)),
                BT_DATA_BYTES(BT_DATA_UUID16_ALL, 0xAA, 0xFE),
                BT_DATA_BYTES(BT_DATA_SVC_DATA16,
                        0xAA, 0xFE,     // Eddystone UUID
                        0x00,           // Eddystone UID frame type
                        0x00,           // Calibrated Tx power at 0m
                        rssi0,  rssi1,  rssi2,  rssi3, 
                        us0[0], us0[1], us1[0], us1[1], 
                        timeConverter.bytes[0], timeConverter.bytes[1], 
                        timeConverter.bytes[2], timeConverter.bytes[3],
                        0x00, 0x00, 0x00, 0x00,
                        0x00, 0x00)
        };

        // /*
        printk("RSSI:  [%04d] [%04d] [%04d] [%04d]  ###   ", rssi0, rssi1, rssi2, rssi3);
        printk("US  :  [%04d | %04d] [%04d | %04d]  ###   ", us0[0], us0[1], us1[0], us1[1]);
        printk("TIME:  [%04d] [%04d] [%04d] [%04d]  \n", timeConverter.bytes[0], timeConverter.bytes[1], 
                timeConverter.bytes[2], timeConverter.bytes[3]);
        // */

        err = bt_le_adv_start(BT_LE_FASTER_ADV, tempAd, ARRAY_SIZE(tempAd), mobileResponseData, ARRAY_SIZE(mobileResponseData));

        k_sleep(K_MSEC(30));

    }
}
