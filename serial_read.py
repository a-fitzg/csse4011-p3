from serial import *
import time
import re
import tago

rssi_list_primary = list()
rssi_list_secondary = list()
us_list = list()



def sendData(rssi_primary, rs_secondary,us):
    MY_DEVICE_TOKEN = '3503290b-05e5-433d-a864-e1b8e7bfbf11'
    my_device = tago.Device(MY_DEVICE_TOKEN)
    data = [{
        'variable': 'rssi1',
        'value': rssi_primary
    },{
        'variable': 'rssi2',
        'value': rssi_secondary
    },{
        'variable': 'ultrasonic',
        'value': us
    }]
    result = my_device.insert(data)
    if result['status']:
        print(result['result'])
    else:
        print(result['message'])


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
        sendData(rssi_list_primary, rssi_list_secondary, us_list)
        time.sleep(0.05)
