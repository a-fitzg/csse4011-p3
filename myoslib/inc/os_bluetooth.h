#ifndef BLUETOOTH_H
#define BLUETOOTH_H

#include <bluetooth/bluetooth.h>
#include <bluetooth/hci.h>

#define DEVICE_NAME         CONFIG_BT_DEVICE_NAME
#define DEVICE_NAME_LEN     (sizeof(DEVICE_NAME) - 1)

#define BT_LE_FASTER_ADV    BT_LE_ADV_PARAM(BT_LE_ADV_OPT_USE_IDENTITY, \
                                            BT_GAP_ADV_FAST_INT_MIN_1, \
                                            BT_GAP_ADV_FAST_INT_MAX_1, \
                                            NULL)

static const struct bt_data new_ad[] = {
    BT_DATA_BYTES(BT_DATA_FLAGS, (BT_LE_AD_GENERAL | BT_LE_AD_NO_BREDR)),
    BT_DATA_BYTES(BT_DATA_UUID16_ALL, 0xAA, 0xFE),
    BT_DATA_BYTES(BT_DATA_SVC_DATA16,
            0xAA, 0xFE,     // Eddystone UUID
            0x00,           // Eddystone UID frame type
            0x00,           // Calibrated Tx power at 0m
            0xDE, 0xAD, 0xBE, 0xEF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x8B, 0xAD, 0xF0, 0x0D, 0x00, 0x00,
            0x00, 0x00)
};


#endif // BLUETOOTH_H
