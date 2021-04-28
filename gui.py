import turtle
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from serial import *
import time
import sys
import io
# from PIL import Image
from io import BytesIO
import re
import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

GRID_X_SIZE = 4
GRID_Y_SIZE = 4

x_beacons = [0, 0, GRID_X_SIZE, GRID_X_SIZE]
y_beacons = [0, GRID_Y_SIZE, GRID_Y_SIZE, 0]
rad_beacons = [1, 1, 1, 1]

mobile_x = 0
mobile_y = 0

valid_x_glob = []
valid_y_glob = []
valid_rad_glob = []

rssi1_glob = None
rssi2_glob = None
rssi3_glob = None
rssi4_glob = None
us1_glob = None
us2_glob = None

main_window = Tk()
main_window.title("GUI")
main_window.geometry("800x700")

top_frame = Frame(main_window, height=100)
centre_frame = Frame(main_window, height=600)
bottom_frame = Frame(main_window, height=300)

top_frame.grid(row=0, sticky="ew")
centre_frame.grid(row=1, sticky="nsew")
bottom_frame.grid(row=2, sticky="ew")

centre_seg1 = Frame(centre_frame, width=240)
centre_seg2 = Frame(centre_frame, width=250)
centre_seg3 = Frame(centre_frame, width=240)

centre_seg1.grid(row=0, column=0, sticky="ns")
centre_seg2.grid(row=0, column=1, sticky="nsew")
centre_seg3.grid(row=0, column=2, sticky="ns")

rssi1_var = StringVar()
rssi2_var = StringVar()
rssi3_var = StringVar()
rssi4_var = StringVar()
us0_var = StringVar()
us1_var = StringVar()
loc_x_var = StringVar()  # use this var for loc x and y
loc_y_var = StringVar()


def raise_error(message):
    messagebox.showerror("Error", message)


def calc_distance(point):
    points = np.array([valid_x_glob, valid_y_glob]).T
    diffs = np.subtract(points, point)
    sum_powers = np.sum(np.power(diffs, 2), axis=1)
    root_sum = np.power(sum_powers, 0.5)
    diff2 = np.subtract(root_sum, valid_rad_glob)

    return diff2


def minimise(point):
    dist = calc_distance(point)
    err = np.linalg.norm(dist / valid_rad_glob)
    return err


def readSerial():
    try:
        serial_conn = Serial(port='/dev/ttyACM0', baudrate=115200)
        rssi1 = 0
        rssi2 = 0
        rssi3 = 0
        rssi4 = 0
        us0H = 0
        us0L = 0
        us1H = 0
        us1L = 0
        time0 = 0
        time1 = 0
        time2 = 0
        time3 = 0
        line = serial_conn.readline().decode()

        bt_data = re.split(',|\r\n', line)
        bt_data = [x for x in bt_data if x != '']
        print(bt_data)
        try:
            if bt_data[0] != '\n':
                rssi1 = int(bt_data[0])
            if bt_data[1] != '\n':
                rssi2 = int(bt_data[1])
            if bt_data[2] != '\n':
                rssi3 = int(bt_data[2])
            if bt_data[3] != '\n':
                rssi4 = int(bt_data[3])
            if bt_data[4] != '\n':
                us0H = int(bt_data[4])
            if bt_data[5] != '\n':
                us0L = int(bt_data[5])
            if bt_data[6] != '\n':
                us1H = int(bt_data[6])
            if bt_data[7] != '\n':
                us1L = int(bt_data[7])
            if bt_data[8] != '\n':
                time0 = int(bt_data[8])
            if bt_data[9] != '\n':
                time1 = int(bt_data[9])
            if bt_data[10] != '\n':
                time2 = int(bt_data[10])
            if bt_data[11] != '\n':
                time3 = int(bt_data[11])
        except IndexError as e:
            pass

        us0 = (us0H << 8) + (us0L)
        us1 = (us1H << 8) + (us1L)
        us0 = us0 / 35  # distance of ultrasonic sensor
        us1 = us1 / 35

        rssi1_glob = rssi1
        rssi2_glob = rssi2
        rssi3_glob = rssi3
        rssi4_glob = rssi4
        us1_glob = us0
        us2_glob = us1

        # convert
        if len(bt_data) < 13:
            rssi1_var.set(rssi1)
            rssi2_var.set(rssi2)
            rssi3_var.set(rssi3)
            rssi4_var.set(rssi4)
        if us0 < 2 and us1 < 2:
            us0_var.set(us0)
            us1_var.set(us1)
    except SerialException as e:
        print("Failed")
        return

    valid_x = []
    valid_y = []
    valid_rad = []

    rssi_vars = [rssi1_glob, rssi2_glob, rssi3_glob, rssi4_glob]
    us_vars = [us1_glob, us2_glob]
    rssi_dists = []

    for i in rssi_vars:
        rssi_dists.append(i)

    for j in range(4):

        # Check RSSI ranges
        if rssi_dists[j] == -128 or rssi_dists[j] >= 0:
            # Discard this reading
            continue
        else:
            valid_x.append(x_beacons[j])
            valid_y.append(y_beacons[j])
            valid_rad.append(10 ** ((-58 - rssi_dists[j]) / 30))

    for j in range(2):
        if us_vars[j] > 4:
            # Discard this reading
            continue
        else:
            valid_x.append(x_beacons[j])
            valid_y.append(y_beacons[j])
            valid_rad.append(us_vars[j])


    # print(f"X: {valid_x} \nY: {valid_y}\nRAD: {valid_rad}")
    valid_x_glob = valid_x
    valid_y_glob = valid_y
    valid_rad_glob = valid_rad

    x_rand = np.random.rand(1)
    y_rand = np.random.rand(1)

    start = (x_rand, y_rand)
    endpos = opt.fmin_powell(minimise, start)

    loc_x_var.set(endpos[0])
    loc_y_var.set(endpos[1])

    #qwertyj = 3456

    main_window.after(200, readSerial)
    time.sleep(0.01)
    return


readSerial()
# RSSI Display
accel_label = Label(centre_seg1, font=("Georgia", 12), text="RSSI Reading: ")
accel_label.grid(column=0, columnspan=2, row=0, padx=20, pady=20)
r_node1 = Label(centre_seg1, font=("Georgia", 8), text="Node1: ")
r_node2 = Label(centre_seg1, font=("Georgia", 8), text="Node2: ")
r_node3 = Label(centre_seg1, font=("Georgia", 8), text="Node3: ")
r_node4 = Label(centre_seg1, font=("Georgia", 8), text="Node4: ")
r_node1.grid(column=0, row=1, padx=10, pady=10)
r_node2.grid(column=0, row=2, padx=10, pady=10)
r_node3.grid(column=0, row=3, padx=10, pady=10)
r_node4.grid(column=0, row=4, padx=10, pady=10)

r1_reading = Label(centre_seg1, font=("Georgia", 8), text="Undetected", textvariable=rssi1_var)
r2_reading = Label(centre_seg1, font=("Georgia", 8), text="Undetected", textvariable=rssi2_var)
r3_reading = Label(centre_seg1, font=("Georgia", 8), text="Undetected", textvariable=rssi3_var)
r4_reading = Label(centre_seg1, font=("Georgia", 8), text="Undetected", textvariable=rssi4_var)
r1_reading.grid(column=1, row=1, padx=10, pady=10)
r2_reading.grid(column=1, row=2, padx=10, pady=10)
r3_reading.grid(column=1, row=3, padx=10, pady=10)
r4_reading.grid(column=1, row=4, padx=10, pady=10)

## Ultrasonic display
us_label = Label(centre_seg2, font=("Georgia", 12), text="Ultrasonic Reading: (m)")
us_label.grid(column=0, columnspan=2, row=0, padx=20, pady=20)
u_node1 = Label(centre_seg2, font=("Georgia", 8), text="U1: ")
u_node2 = Label(centre_seg2, font=("Georgia", 8), text="U2: ")
u1_reading = Label(centre_seg2, font=("Georgia", 8), text="Undetected", textvariable=us0_var)
u2_reading = Label(centre_seg2, font=("Georgia", 8), text="Undetected", textvariable=us1_var)
u1_reading.grid(column=1, row=1, padx=10, pady=10)
u2_reading.grid(column=1, row=2, padx=10, pady=10)

# Location
loc_label = Label(centre_seg3, font=("Georgia", 12), text="Location: ")
loc_label.grid(column=0, columnspan=2, row=0, padx=20, pady=20)
loc_x = Label(centre_seg3, font=("Georgia", 8), text="x: ")
loc_x.grid(column=0, row=1, padx=10, pady=10)
loc_y = Label(centre_seg3, font=("Georgia", 8), text="y: ")
loc_y.grid(column=0, row=2, padx=10, pady=10)
locx = Label(centre_seg3, font=("Georgia", 8), text="Undetected", textvariable=loc_x_var)
locy = Label(centre_seg3, font=("Georgia", 8), text="Undetected", textvariable=loc_y_var)
locx.grid(column=1, row=1, padx=10, pady=10)
locy.grid(column=1, row=2, padx=10, pady=10)
main_window.mainloop()
