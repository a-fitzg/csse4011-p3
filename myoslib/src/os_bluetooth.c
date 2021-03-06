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

// Initial advertising data for static nodes (overriden as soon as static node
// enters cyclic executive)
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

// Advertising response data for static nodes
const struct bt_data staticResponseData[] = {
    BT_DATA(BT_DATA_NAME_COMPLETE, DEVICE_NAME, DEVICE_NAME_LEN),
};

/**
 * @brief       Check if two bluetooth addresses are equal
 * @param       address1: First address
 * @param       address2: Second address
 * @retval      true if addresses are equal, false if not equal
 */
uint8_t addressesEqual(bt_addr_t address1, bt_addr_t address2) {

    // Iterate through all address fields and see if they are equal
    // If ANY field does not match, return false
    for (uint8_t i = 0; i < 6; i++) {

        if (address1.val[i] != address2.val[i]) {

            // Found non-matching field
            return false;
        }
    }

    return true;

}

/**
 * @brief       Callback function for mobile node scan
 * @param       addr:       Address of scan response
 * @param       rssi:       RSSI strength of response
 * @param       adv_type:   Response message type
 * @param       buf:        Data buffer of message
 */
void bt_mobileCallback(const bt_addr_le_t *addr, int8_t rssi, uint8_t adv_type,
		    struct net_buf_simple *buf) {
    
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
        while (k_msgq_put(&os_QueueBtNodeMessage, &nodeQueueItem, K_NO_WAIT) 
                != 0) {

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
        nodeQueueItem.rssi = rssi;
        memcpy(&nodeQueueItem.payload, &payload, sizeof(payload));

        // Send off message to listening thread
        while (k_msgq_put(&os_QueueBtNodeMessage, &nodeQueueItem, K_NO_WAIT) 
                != 0) {

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
        nodeQueueItem.rssi = rssi;
        memcpy(&nodeQueueItem.payload, &payload, sizeof(payload));

        // Send off message to listening thread
        while (k_msgq_put(&os_QueueBtNodeMessage, &nodeQueueItem, K_NO_WAIT) 
                != 0) {

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
        nodeQueueItem.rssi = rssi;
        memcpy(&nodeQueueItem.payload, &payload, sizeof(payload));

        // Send off message to listening thread
        while (k_msgq_put(&os_QueueBtNodeMessage, &nodeQueueItem, K_NO_WAIT) 
                != 0) {

            k_msgq_purge(&os_QueueBtNodeMessage);
        }
    }

    // Listen for messages from node 5
    if (addressesEqual(addr->a, nodeList[4].node.address)) {

        uint8_t payload[PAYLOAD_SIZE];
        // Make up the payload array
        for (uint8_t i = 0; i < PAYLOAD_SIZE; i++) {

            payload[i] = buf->data[i + PAYLOAD_BUFFER_OFFSET];
        }
        
        // Make up the message item to send to listening thread
        NodeQueueItem nodeQueueItem;
        nodeQueueItem.index = 4;
        nodeQueueItem.rssi = rssi;
        payload[0] = 0;
        payload[1] = buf->data[PAYLOAD_BUFFER_OFFSET - 1];
        memcpy(&nodeQueueItem.payload, &payload, sizeof(payload));
        

        // Send off message to listening thread
        while (k_msgq_put(&os_QueueBtNodeMessage, &nodeQueueItem, K_NO_WAIT) 
                != 0) {

            k_msgq_purge(&os_QueueBtNodeMessage);
        }
    }

    // Listen for messages from node 6
    else if (addressesEqual(addr->a, nodeList[5].node.address)) {

        uint8_t payload[PAYLOAD_SIZE];
        // Make up the payload array
        for (uint8_t i = 0; i < PAYLOAD_SIZE; i++) {

            payload[i] = buf->data[i + PAYLOAD_BUFFER_OFFSET];
        }
        
        // Make up the message item to send to listening thread
        NodeQueueItem nodeQueueItem;
        nodeQueueItem.index = 5;
        nodeQueueItem.rssi = rssi;
        payload[0] = 0;
        payload[1] = buf->data[PAYLOAD_BUFFER_OFFSET - 1];
        memcpy(&nodeQueueItem.payload, &payload, sizeof(payload));

        // Send off message to listening thread
        while (k_msgq_put(&os_QueueBtNodeMessage, &nodeQueueItem, K_NO_WAIT) 
                != 0) {

            k_msgq_purge(&os_QueueBtNodeMessage);
        }
    }

    // Listen for messages from node 7
    else if (addressesEqual(addr->a, nodeList[6].node.address)) {

        uint8_t payload[PAYLOAD_SIZE];
        // Make up the payload array
        for (uint8_t i = 0; i < PAYLOAD_SIZE; i++) {

            payload[i] = buf->data[i + PAYLOAD_BUFFER_OFFSET];
        }
        
        // Make up the message item to send to listening thread
        NodeQueueItem nodeQueueItem;
        nodeQueueItem.index = 6;
        nodeQueueItem.rssi = rssi;
        payload[0] = 0;
        payload[1] = buf->data[PAYLOAD_BUFFER_OFFSET - 1];
        memcpy(&nodeQueueItem.payload, &payload, sizeof(payload));

        // Send off message to listening thread
        while (k_msgq_put(&os_QueueBtNodeMessage, &nodeQueueItem, K_NO_WAIT) 
                != 0) {

            k_msgq_purge(&os_QueueBtNodeMessage);
        }
    }

    // Listen for messages from node 8
    else if (addressesEqual(addr->a, nodeList[7].node.address)) {

        uint8_t payload[PAYLOAD_SIZE];
        // Make up the payload array
        for (uint8_t i = 0; i < PAYLOAD_SIZE; i++) {

            payload[i] = buf->data[i + PAYLOAD_BUFFER_OFFSET];
        }
        
        // Make up the message item to send to listening thread
        NodeQueueItem nodeQueueItem;
        nodeQueueItem.index = 7;
        nodeQueueItem.rssi = rssi;
        payload[0] = 0;
        payload[1] = buf->data[PAYLOAD_BUFFER_OFFSET - 1];
        memcpy(&nodeQueueItem.payload, &payload, sizeof(payload));

        // Send off message to listening thread
        while (k_msgq_put(&os_QueueBtNodeMessage, &nodeQueueItem, K_NO_WAIT) 
                != 0) {

            k_msgq_purge(&os_QueueBtNodeMessage);
        }
    }
}

/**
 * @brief   Initialisation function for static beacon bluetooth advertising
 * @param   err:    Error value - from calling function
 */
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
    err = bt_le_adv_start(BT_LE_FASTER_ADV, staticAdData, 
            ARRAY_SIZE(staticAdData), staticResponseData, 
            ARRAY_SIZE(staticResponseData));

    if (err) {
        printk("Advertising failed to start (err %d)\n", err);
        return;
    }

    bt_id_get(&addr, &count);
    bt_addr_le_to_str(&addr, addr_s, sizeof(addr_s));

    printk("Beacon started, advertising as %s\n", addr_s);
}

/**
 * @brief   Initialisation function for mobile beacon bluetooth advertising
 * @param   err:    Error value - from calling function
 */
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
    err = bt_le_adv_start(BT_LE_FASTER_ADV, staticAdData, 
            ARRAY_SIZE(staticAdData), staticResponseData, 
            ARRAY_SIZE(staticResponseData));

    if (err) {
        printk("Advertising failed to start (err %d)\n", err);
        return;
    }

    bt_id_get(&addr, &count);
    bt_addr_le_to_str(&addr, addr_s, sizeof(addr_s));

    printk("Beacon started, advertising as %s\n", addr_s);

}

/**
 * @brief   Thread routine for mobile node queue listening - this thread is 
 *          responsible for listening on the queue of incoming bluetooth
 *          messages from static nodes, and saving their values
 * @param   args:   Array of arguments
 */
uint8_t os_bluetoothMobileListen(void* args) {

    NodeQueueItem nodeQueueItem;

    while (1) {

        // Get next item from queue
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

                    nodeList[i].node.ultrasonic[0] = payload[0];
                    nodeList[i].node.ultrasonic[1] = payload[1];

                    break;
                }
            }
        }


#ifdef DEBUG_PRINT

        printk("message [%d - RSSI: %d]: ", nodeQueueItem.index, 
                nodeQueueItem.rssi);
    
        for (uint8_t i = 0; i < 16; i++) {

            printk("%d:", nodeQueueItem.payload[i]);
        }
        
        printk("\n");

#endif  // DEBUG_PRINT
        k_mutex_unlock(&os_MutexNodeList);
    }

    return 0;

}

