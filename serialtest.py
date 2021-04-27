from serial import * 
import time
import re

def readSerial():
    try:
        line = ser.readline()
        bt_data = re.split(',|\n', line)
        value = []
        print(bt_data)
    except SerialException as e:
        print("Failed")
        return

ser = Serial(port="COM11", baudrate=115200, parity=PARITY_NONE, bytesize=EIGHTBITS, stopbits=STOPBITS_ONE, timeout=0)

while True:
    readSerial()
    time.sleep(1)
