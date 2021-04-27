/* main.c - Application main entry point */

/*
 * Copyright (c) 2015-2016 Intel Corporation
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/types.h>
#include <stddef.h>
#include <sys/printk.h>
#include <sys/util.h>
#include <bluetooth/bluetooth.h>
#include <bluetooth/hci.h>

#include <os_bluetooth.h>

/*
#define DEVICE_NAME CONFIG_BT_DEVICE_NAME
#define DEVICE_NAME_LEN (sizeof(DEVICE_NAME) - 1)

#define BT_LE_FASTER_ADV    BT_LE_ADV_PARAM(BT_LE_ADV_OPT_USE_IDENTITY, \
                                            BT_GAP_ADV_FAST_INT_MIN_1, \
						                    BT_GAP_ADV_FAST_INT_MAX_1, \
						                    NULL)
*/

/*
 * Set Advertisement data. Based on the Eddystone specification:
 * https://github.com/google/eddystone/blob/master/protocol-specification.md
 * https://github.com/google/eddystone/tree/master/eddystone-url
 */
/*
static const struct bt_data ad[] = {
    // 02 01 04 03 03
	BT_DATA_BYTES(BT_DATA_FLAGS, BT_LE_AD_NO_BREDR),
    // aa fe 10 16
	BT_DATA_BYTES(BT_DATA_UUID16_ALL, 0xaa, 0xfe),
    // aa fe 10 00 00 [wikipedia.org]
	BT_DATA_BYTES(BT_DATA_SVC_DATA16,
		      0xaa, 0xfe, // Eddystone UUID
		      0x10, // Eddystone-URL frame type
		      0x00, // Calibrated Tx power at 0m
		      0x00, // URL Scheme Prefix http://www.
		      'w', 'i', 'k', 'i', 'p', 'e', 'd', 'i', 'a',
		      0x08) // .org
};
*/

/*
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
*/

// Set Scan Response data
/*
static const struct bt_data sd[] = {
	BT_DATA(BT_DATA_NAME_COMPLETE, DEVICE_NAME, DEVICE_NAME_LEN),
};
*/

/*
static void bt_ready(int err)
{
	char addr_s[BT_ADDR_LE_STR_LEN];
	bt_addr_le_t addr = {0};
	size_t count = 1;

	if (err) {
		printk("Bluetooth init failed (err %d)\n", err);
		return;
	}

	printk("Bluetooth initialized\n");

	// Start advertising
	err = bt_le_adv_start(BT_LE_FASTER_ADV, new_ad, ARRAY_SIZE(new_ad),
			      sd, ARRAY_SIZE(sd));
	if (err) {
		printk("Advertising failed to start (err %d)\n", err);
		return;
	}


	bt_id_get(&addr, &count);
	bt_addr_le_to_str(&addr, addr_s, sizeof(addr_s));

	printk("Beacon started, advertising as %s\n", addr_s);
}
*/


static const struct bt_data response[] = {
    BT_DATA(BT_DATA_NAME_COMPLETE, DEVICE_NAME, DEVICE_NAME_LEN),
};

void main(void) {

	int err;

	printk("Starting Beacon Demo\n");

	// Initialize the Bluetooth Subsystem
	err = bt_enable(os_bluetooth_staticBeaconInit);
	if (err) {
		printk("Bluetooth init failed (err %d)\n", err);
	}

    uint8_t iter = 0;
    while (1) {

        err = bt_le_adv_stop();

        const struct bt_data tempAd[] = {
                BT_DATA_BYTES(BT_DATA_FLAGS, (BT_LE_AD_GENERAL | BT_LE_AD_NO_BREDR)),
                BT_DATA_BYTES(BT_DATA_UUID16_ALL, 0xAA, 0xFE),
                BT_DATA_BYTES(BT_DATA_SVC_DATA16,
                        0xAA, 0xFE,     // Eddystone UUID
                        0x00,           // Eddystone UID frame type
                        0x00,           // Calibrated Tx power at 0m
                        0xDE, 0xAD, 0xBE, 0xEF, 0x12, 0x34, 0x56, 0x78, 0x90, iter,
                        0x8B, 0xAD, 0xF0, 0x0D, 0xAB, 0xCD,
                        0x00, 0x00)
        };

        err = bt_le_adv_start(BT_LE_FASTER_ADV, tempAd, ARRAY_SIZE(tempAd), response, ARRAY_SIZE(response));
        iter++;
        k_sleep(K_MSEC(30));
    }
}
