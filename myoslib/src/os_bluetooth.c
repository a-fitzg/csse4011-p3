/**
 ******************************************************************************
 * @file            myoslib/src/os_bluetooth.c
 * @author          Alexander FitzGerald - 45330874
 * @date            10042020
 * @brief           Bluetooth driver functions for static, mobile, and base node
 ******************************************************************************
 * EXTERNAL FUNCTIONS
 ******************************************************************************
 *
 ******************************************************************************
 */

#include <zephyr.h>
#include <zephyr/types.h>
#include <stddef.h>
#include <sys/printk.h>
#include <sys/util.h>
#include <device.h>
#include <devicetree.h>
#include <bluetooth/bluetooth.h>
#include <bluetooth/hci.h>

#include <os_bluetooth.h>

static const struct bt_data staticAdData[] = {

    BT_DATA_BYTES(BT_DATA_FLAGS, (BT_LE_AD_GENERAL | BT_LE_AD_NO_BREDR)),
    BT_DATA_BYTES(BT_DATA_UUID16_ALL, 0xAA, 0xFE),
    BT_DATA_BYTES(BT_DATA_SVC_DATA16,
            0xAA, 0xFE,     // Eddystone UUID
            0x00,           // Eddystone UID frame type
            0x00,           // Calibrated Tx power at 0m
            0x22, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00)     // These have to be 0x00
}; 

/*
static const struct bt_data mobileAdData[] = {

    BT_DATA_BYTES(BT_DATA_FLAGS, (BT_LE_AD_GENERAL | BT_LE_AD_NO_BREDR)),
    BT_DATA_BYTES(BT_DATA_UUID16_ALL, 0xAA, 0xFE),
    BT_DATA_BYTES(BT_DATA_SVC_DATA16,
            0xAA, 0xFE,     // Eddystone UUID
            0x00,           // Eddystone UID frame type
            0x00,           // Calibrated Tx power at 0m
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00)     // These have to be 0x00

};
*/

const struct bt_data staticResponseData[] = {
    BT_DATA(BT_DATA_NAME_COMPLETE, DEVICE_NAME, DEVICE_NAME_LEN),
};


uint8_t addressesEqual(bt_addr_t address1, bt_addr_t address2) {

    // Iterate through all address fields and see if they are equal
    // If ANY field does not match, return false
    for (uint8_t i = 0; i < 6; i++) {

        if (address1.val[i] != address2.val[i]) {

            return false;
        }
    }

    return true;

}


void scan_cb(const bt_addr_le_t *addr, int8_t rssi, uint8_t adv_type,
		    struct net_buf_simple *buf) {
    
    /*
    //if (rssi > 50) {
    printk("Found device [type: %d,  addr: %02x:%02x:%02x:%02x:%02x:%02x,  RSSI: %d,  len: %d,  DAT: %x]\n", addr->type, 
            addr->a.val[0], 
            addr->a.val[1],
            addr->a.val[2],
            addr->a.val[3],
            addr->a.val[4],
            addr->a.val[5],
            rssi, buf->len,
            *buf->data);
    //}
    */
    
    /*
    if (addr->a.val[0] == 0xD2 && 
        addr->a.val[1] == 0x3D &&
        addr->a.val[2] == 0x4E &&
        addr->a.val[3] == 0x14 &&
        addr->a.val[4] == 0x23 &&
        addr->a.val[5] == 0xD9) {

        // This is our beacon
        LOG_INF("Beacon A ---");
        //printk("--- BEACON A\n");
        
        printk("Found beacon A [RSSI: %d] DAT:[", rssi);
        for (uint8_t i = 0; i < buf->len; i++) {
            printk("%02x", buf->data[i]);
            if (i < (buf->len) - 1) {
                printk("|");
            }
        }
        printk("]\n");
        
    }
    
    if (addr->a.val[0] == 0xAF && 
        addr->a.val[1] == 0xDE &&
        addr->a.val[2] == 0xCD &&
        addr->a.val[3] == 0xD4 &&
        addr->a.val[4] == 0x38 &&
        addr->a.val[5] == 0xE1) {

        // This is our beacon
        LOG_WRN("--- Beacon B");
        //printk("BEACON B ---\n");
        
        printk("######## Found beacon B [RSSI: %d] DAT:[", rssi);
        for (uint8_t i = 0; i < buf->len; i++) {
            printk("%02x", buf->data[i]);
            if (i < (buf->len) - 1) {
                printk("|");
            }
        }
        printk("]\n");
        
    }
    */

    // Listen for messages from node 1
    if (addressesEqual(addr->a, nodeList[0].node.address)) {

        uint8_t payload[PAYLOAD_SIZE];
        // Make up the payload array
        for (uint8_t i = 0; i < PAYLOAD_SIZE; i++) {

            payload[i] = buf->data[i + PAYLOAD_BUFFER_OFFSET];
        }
        
        // Make up the message item to send to listening thread
        NodeQueueItem nodeQueueItem;
        nodeQueueItem.index = 0;
        nodeQueueItem.rssi = rssi;
        memcpy(&nodeQueueItem.payload, &payload, sizeof(payload));

        // Send off message to listening thread
        while (k_msgq_put(&os_QueueBtNodeMessage, &nodeQueueItem, K_NO_WAIT) != 0) {

            k_msgq_purge(&os_QueueBtNodeMessage);
        }
    }

    // Listen for messages from node 2
    else if (addressesEqual(addr->a, nodeList[1].node.address)) {

        uint8_t payload[PAYLOAD_SIZE];
        // Make up the payload array
        for (uint8_t i = 0; i < PAYLOAD_SIZE; i++) {

            payload[i] = buf->data[i + PAYLOAD_BUFFER_OFFSET];
        }
        
        // Make up the message item to send to listening thread
        NodeQueueItem nodeQueueItem;
        nodeQueueItem.index = 1;
        memcpy(&nodeQueueItem.payload, &payload, sizeof(payload));

        // Send off message to listening thread
        while (k_msgq_put(&os_QueueBtNodeMessage, &nodeQueueItem, K_NO_WAIT) != 0) {

            k_msgq_purge(&os_QueueBtNodeMessage);
        }
    }

    // Listen for messages from node 3
    else if (addressesEqual(addr->a, nodeList[2].node.address)) {

        uint8_t payload[PAYLOAD_SIZE];
        // Make up the payload array
        for (uint8_t i = 0; i < PAYLOAD_SIZE; i++) {

            payload[i] = buf->data[i + PAYLOAD_BUFFER_OFFSET];
        }
        
        // Make up the message item to send to listening thread
        NodeQueueItem nodeQueueItem;
        nodeQueueItem.index = 2;
        memcpy(&nodeQueueItem.payload, &payload, sizeof(payload));

        // Send off message to listening thread
        while (k_msgq_put(&os_QueueBtNodeMessage, &nodeQueueItem, K_NO_WAIT) != 0) {

            k_msgq_purge(&os_QueueBtNodeMessage);
        }
    }

    // Listen for messages from node 4
    else if (addressesEqual(addr->a, nodeList[3].node.address)) {

        uint8_t payload[PAYLOAD_SIZE];
        // Make up the payload array
        for (uint8_t i = 0; i < PAYLOAD_SIZE; i++) {

            payload[i] = buf->data[i + PAYLOAD_BUFFER_OFFSET];
        }
        
        // Make up the message item to send to listening thread
        NodeQueueItem nodeQueueItem;
        nodeQueueItem.index = 3;
        memcpy(&nodeQueueItem.payload, &payload, sizeof(payload));

        // Send off message to listening thread
        while (k_msgq_put(&os_QueueBtNodeMessage, &nodeQueueItem, K_NO_WAIT) != 0) {

            k_msgq_purge(&os_QueueBtNodeMessage);
        }
    }
}


void os_bluetooth_staticBeaconInit(int err) {

    char addr_s[BT_ADDR_LE_STR_LEN];
    bt_addr_le_t addr = {0};
    size_t count = 1;

    if (err) {
        printk("Bluetooth init failed (err %d)\n", err);                        
        return;
    }

    printk("Bluetooth initialized\n");

    // Start advertising
    err = bt_le_adv_start(BT_LE_FASTER_ADV, staticAdData, ARRAY_SIZE(staticAdData),
                  staticResponseData, ARRAY_SIZE(staticResponseData));
    if (err) {
        printk("Advertising failed to start (err %d)\n", err);
        return;
    }

    bt_id_get(&addr, &count);
    bt_addr_le_to_str(&addr, addr_s, sizeof(addr_s));

    printk("Beacon started, advertising as %s\n", addr_s);
}


void os_bluetooth_mobileBeaconInit(int err) {

    char addr_s[BT_ADDR_LE_STR_LEN];
    bt_addr_le_t addr = {0};
    size_t count = 1;

    if (err) {
        printk("Bluetooth init failed (err %d)\n", err);                        
        return;
    }

    printk("Bluetooth initialized\n");

    // Start advertising
    err = bt_le_adv_start(BT_LE_FASTER_ADV, staticAdData, ARRAY_SIZE(staticAdData),
                  staticResponseData, ARRAY_SIZE(staticResponseData));
    if (err) {
        printk("Advertising failed to start (err %d)\n", err);
        return;
    }

    bt_id_get(&addr, &count);
    bt_addr_le_to_str(&addr, addr_s, sizeof(addr_s));

    printk("Beacon started, advertising as %s\n", addr_s);
}



uint8_t os_bluetoothMobileListen(void* args) {

    NodeQueueItem nodeQueueItem;

    while (1) {

        k_msgq_get(&os_QueueBtNodeMessage, &nodeQueueItem, K_FOREVER);

        // Unpack incoming message into bytes

        uint8_t index = nodeQueueItem.index;
        int8_t  rssi  = nodeQueueItem.rssi;
        uint8_t payload[PAYLOAD_SIZE];
        memcpy(&payload, &nodeQueueItem.payload, sizeof(payload));

        // Only 1 thread should access the node list at a time
        k_mutex_lock(&os_MutexNodeList, K_FOREVER);
        for (uint8_t i = 0; i < NUM_STATIC_NODES; i++) {

            // Look for item in node list with given index
            if (nodeList[i].index == index) {

                // We have the correct node item
                nodeList[i].node.rssi = rssi;
                // If this item is an ultrasonic sensor, save additional
                // ultrasonic ranging information
                if (nodeList[i].node.hasUltrasonic) {

                    // Convert byte array into double
                    union {
                        unsigned char bytes[sizeof(double)];
                        double        us;
                    } usConverter;
                    
                    // Copy first 8 bytes from payload into conversion union
                    memcpy(&usConverter.bytes, &payload, sizeof(double));

                    nodeList[i].node.ultrasonic = usConverter.us;

                    break;
                }
            }
        }

        
        // 
        //nodeList[nodeQueueItem.index].node;

        printk("message [%d - RSSI: %d]: ", nodeQueueItem.index, nodeQueueItem.rssi);
    
        for (uint8_t i = 0; i < 16; i++) {

            printk("%d:", nodeQueueItem.payload[i]);
        }
        
        //printk("%d", message);
        printk("\n");
        //k_msleep(1);
        
        k_mutex_unlock(&os_MutexNodeList);
    }

    return 0;

}

