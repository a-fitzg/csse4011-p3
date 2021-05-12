from serial import *
import time
import re
import tago

rssi_list_primary = list()
rssi_list_secondary = list()
us_list_primary = list()
us_list_secondary = list()

temp_list_us = []


def sendData(rssi_primary, rssi_secondary,us1, us2):
    MY_DEVICE_TOKEN = '3503290b-05e5-433d-a864-e1b8e7bfbf11'
    my_device = tago.Device(MY_DEVICE_TOKEN)
    try:
        data = [{
            'variable': 'rssi1',
            'value': rssi_primary
        },{
            'variable': 'rssi2',
            'value': rssi_secondary
        },{
            'variable': 'ultrasonic1',
            'value': us1
        },{
            'variable': 'ultrasonic2',
            'value': us2
        },{
            'variable': 'rssi1_1',
            'value': rssi_primary[0]
        },{
            'variable': 'rssi1_2',
            'value': rssi_primary[1]
        },{
            'variable': 'rssi1_3',
            'value': rssi_primary[2]
        },{
            'variable': 'rssi1_4',
            'value': rssi_primary[3]
        },{
            'variable': 'rssi1_5',
            'value': rssi_primary[4]
        },{
            'variable': 'rssi1_6',
            'value': rssi_primary[5]
        },{
            'variable': 'rssi1_7',
            'value': rssi_primary[6]
        },{
            'variable': 'rssi1_8',
            'value': rssi_secondary[7]
        },{
            'variable': 'rssi2_1',
            'value': rssi_secondary[0]
        },{
            'variable': 'rssi2_2',
            'value': rssi_secondary[1]
        },{
            'variable': 'rssi2_3',
            'value': rssi_secondary[2]
        },{
            'variable': 'rssi2_4',
            'value': rssi_secondary[3]
        },{
            'variable': 'rssi2_5',
            'value': rssi_secondary[4]
        },{
            'variable': 'rssi2_6',
            'value': rssi_secondary[5]
        },{
            'variable': 'rssi2_7',
            'value': rssi_secondary[6]
        },{
            'variable': 'rssi2_8',
            'value': rssi_secondary[7]
        },{
            'variable': 'ultrasonic1',
            'value': us[0]
        },{
            'variable': 'ultrasonic2',
            'value': us[1]
        },{
            'variable': 'ultrasonic3',
            'value': us[2]
        },{
            'variable': 'ultrasonic4',
            'value': us[3]
        }]
        print('here')
        result = my_device.insert(data)
    except IndexError:
        return

    print("##########  SENT  ###########")

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
    ser = Serial(port="COM8", baudrate=115200, parity=PARITY_NONE, bytesize=EIGHTBITS, stopbits=STOPBITS_ONE,
                 timeout=0)

    while True:
        data_tokens = readSerial()
        if len(data_tokens) != 17:
            continue
        temp_list_rssi = [int(i) for i in data_tokens[0:8]]
        if data_tokens[-1] == 0:
            temp_list_us = [int(i) for i in data_tokens[8:16]]
        if int(data_tokens[-1]) == 0 or int(data_tokens[-1]) == 1:
            if int(data_tokens[-1]) == 0:
                # Primary node
                rssi_list_primary = temp_list_rssi.copy()
                print(f"NODE 0: RSSI: {{{rssi_list_primary}}}, US: {{{temp_list_us}}} ")
            if int(data_tokens[-1]) == 1:
                # Secondary node
                rssi_list_secondary = temp_list_rssi.copy()
                print(f"NODE 1: {{{rssi_list_secondary}}}, US: {{{temp_list_us}}}")
        else:
            # Dodgy node number
            pass
        sendData(rssi_list_primary, rssi_list_secondary, us_list)
        time.sleep(0.05)
