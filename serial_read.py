from serial import *
import time
import re

rssi_list_primary = list()
rssi_list_secondary = list()
us_list = list()


def readSerial():
    try:
        line = ser.readline().decode()
        bt_data = re.split(',|\n\r', line)
        bt_data[-1] = bt_data[-1].rstrip('\n').rstrip('\r')
        value = []
        return bt_data
        #print(bt_data)
    except SerialException as e:
        print("Failed")
        return


if __name__ == "__main__":
    ser = Serial(port="/dev/ttyACM0", baudrate=115200, parity=PARITY_NONE, bytesize=EIGHTBITS, stopbits=STOPBITS_ONE,
                 timeout=0)

    while True:
        data_tokens = readSerial()
        if len(data_tokens) != 17:
            continue
        temp_list_rssi = [int(i) for i in data_tokens[0:8]]
        temp_list_us = [int(i) for i in data_tokens[8:16]]
        if int(data_tokens[-1]) == 0:
            # Primary node
            rssi_list_primary = temp_list_rssi.copy()
            print(f"NODE 0: RSSI: {{{rssi_list_primary}}}, US: {{{temp_list_us}}} ")
        elif int(data_tokens[-1]) == 1:
            # Secondary node
            rssi_list_secondary = temp_list_rssi.copy()
            print(f"NODE 1: {{{rssi_list_secondary}}}, US: {{{temp_list_us}}}")
        else:
            # Dodgy node number
            pass

        time.sleep(0.05)
