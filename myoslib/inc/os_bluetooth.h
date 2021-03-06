#ifndef BLUETOOTH_H
#define BLUETOOTH_H

#include <bluetooth/bluetooth.h>
#include <bluetooth/hci.h>

#define DEVICE_NAME             CONFIG_BT_DEVICE_NAME
#define DEVICE_NAME_LEN         (sizeof(DEVICE_NAME) - 1)

#define NUM_STATIC_NODES        8
#define PAYLOAD_SIZE            16
#define PAYLOAD_BUFFER_OFFSET   13
#define NODE_QUEUE_ALIGNMENT    32

#define BT_QUEUE_LENGTH         32
#define BT_THREAD_STACK_SIZE    500
#define BT_THREAD_PRIORITY      5

#define false                   0
#define true                    1

#define BT_LE_FASTER_ADV        BT_LE_ADV_PARAM(BT_LE_ADV_OPT_USE_IDENTITY, \
                                                BT_GAP_ADV_FAST_INT_MIN_1, \
                                                BT_GAP_ADV_FAST_INT_MAX_1, \
                                                NULL)

// Properties of a static node
typedef struct {
    bt_addr_t   address;
    uint8_t     hasUltrasonic;
    int8_t      rssi;
    uint8_t     ultrasonic[2];
} StaticNode;

// Static node list item, each with an index and node properties
typedef struct {
    uint8_t     index;
    StaticNode  node;
} NodeListItem;

// Items on the node message queue
typedef struct {
    uint8_t     index;
    int8_t      rssi;
    uint8_t     payload[PAYLOAD_SIZE];
} NodeQueueItem;

// Mutex for accessing list of node properties
extern struct k_mutex os_MutexNodeList;

// List of nodes and their properties
// ##### MUST USE MUTEX (os_MutexNodeList) TO ACCESS THIS LIST #####
extern NodeListItem nodeList[NUM_STATIC_NODES];

// Message queue for incoming bluetooth messages (from static nodes)
extern struct k_msgq os_QueueBtNodeMessage;

// Function prototypes - more detailed top comments in source file
uint8_t addressesEqual(bt_addr_t, bt_addr_t);
void bt_mobileCallback(const bt_addr_le_t*, int8_t, uint8_t,
        struct net_buf_simple*);
void os_bluetooth_staticBeaconInit(int);
void os_bluetooth_mobileBeaconInit(int);
uint8_t os_bluetoothMobileListen(void*);

#endif // BLUETOOTH_H
