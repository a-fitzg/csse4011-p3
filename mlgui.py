import tago
import numpy as np
import scipy.optimize as opt
from sklearn.neighbors import KNeighborsClassifier   
from pykalman import KalmanFilter
import matplotlib.pyplot as plt
import time
import matplotlib.animation as animation
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import math

MY_DEVICE_TOKEN = '3503290b-05e5-433d-a864-e1b8e7bfbf11'
my_device = tago.Device(MY_DEVICE_TOKEN)

main_window = Tk()
main_window.title("GUI")
main_window.geometry("800x700")
significant_digits = 3

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

mobile1x_var = StringVar()
mobile1y_var = StringVar()
mobile2x_var = StringVar()
mobile2y_var = StringVar()

GRID_X_SIZE = 8
GRID_Y_SIZE = 4

NUM_STATIC_NODES = 8

RSSI_WEIGHT = 1
US_WEIGHT = 0.001

X_BEACONS = [0, GRID_X_SIZE, GRID_X_SIZE / 3, 2 * GRID_X_SIZE / 3,
             GRID_X_SIZE, 0, GRID_X_SIZE / 3, 2 * GRID_X_SIZE / 3]
Y_BEACONS = [GRID_Y_SIZE, GRID_Y_SIZE, 0, 0,
             0, 0, GRID_Y_SIZE, GRID_Y_SIZE]
US_X_BEACONS = [GRID_X_SIZE, 0, 0, GRID_X_SIZE]
US_Y_BEACONS = [0, 0, GRID_Y_SIZE , GRID_Y_SIZE]

valid_x_glob_m1 = []
valid_y_glob_m1 = []
valid_rad_glob_m1 = []
valid_x_glob_m2 = []
valid_y_glob_m2 = []
valid_rad_glob_m2 = []
valid_us_glob = []

temp2 = []


def calc_distance_m1(point):
    points = np.array([valid_x_glob_m1, valid_y_glob_m1]).T
    diffs = np.subtract(points, point)
    sum_powers = np.sum(np.power(diffs, 2), axis=1)
    root_sum = np.power(sum_powers, 0.5)
    diff2 = np.subtract(root_sum, valid_rad_glob_m1)
    return diff2


def minimise_m1(point):
    weights = []
    weights = [RSSI_WEIGHT for _ in range(len(valid_rad_glob_m1))]
    weights[-4:] = 4 * [US_WEIGHT]

    dist = calc_distance_m1(point)
    err = np.linalg.norm(dist / [a * b for a, b in zip(valid_rad_glob_m1, weights)])
    return err


def calc_distance_m2(point):
    points = np.array([valid_x_glob_m2, valid_y_glob_m2]).T
    diffs = np.subtract(points, point)
    sum_powers = np.sum(np.power(diffs, 2), axis=1)
    root_sum = np.power(sum_powers, 0.5)
    diff2 = np.subtract(root_sum, valid_rad_glob_m2)
    return diff2


def minimise_m2(point):
    weights = []
    weights = [RSSI_WEIGHT for _ in range(len(valid_rad_glob_m2))]
    weights[-4:] = 4 * [US_WEIGHT]

    dist = calc_distance_m2(point)
    err = np.linalg.norm(dist / [a * b for a, b in zip(valid_rad_glob_m1, weights)])
    return err


def get_trainingmodel():
    ITERATE_X = 8
    ITERATE_Y = 10
    X_train = []
    Y_train = []
    temp_x = []
    temp_y = []
    count = 0
    findData = my_device.find({'variable':'trainingset'})
    for d in findData['result']:
        temp = d['value']

    r_n = [int(s) for s in temp.split(',')]
    for x in r_n:
        if count < ITERATE_X:
            temp_x.append(x)
            count += 1
        elif count >= ITERATE_X and count < ITERATE_Y:
            temp_y.append(x)
            count += 1
        else:
            X_train.append(temp_x)
            Y_train.append(temp_y)
            temp_x = []
            temp_y = []
            temp_x.append(x)
            count = 1
    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(X_train,Y_train)
 
    return model

def Kalman(raw_data):
    kf = KalmanFilter(initial_state_mean=[0,0], n_dim_obs=2)
    measurements = np.asarray(raw_data)  # 2 observations
    initial_state_mean = [measurements[0, 0],
                        0,
                        measurements[0, 1],
                        0]
    transition_matrix = [[1, 1, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, 1],
                        [0, 0, 0, 1]]
    observation_matrix = [[1, 0, 0, 0],
                        [0, 0, 1, 0]]

    kf1 = KalmanFilter(transition_matrices = transition_matrix,
                    observation_matrices = observation_matrix,
                    initial_state_mean = initial_state_mean)
    kf1 = kf1.em(measurements, n_iter=5)
    (smoothed_state_means, smoothed_state_covariances) = kf1.smooth(measurements)
    x = smoothed_state_means[:, 0]
    y = smoothed_state_means[:, 2]
    # mean_x = mean(x)
    # mean_y = mean(y)
    # print(mean_x)
    # print(mean_y)
    # print(smoothed_state_means)
    mean_x = (sum(x)) / len(x)
    mean_y = (sum(y)) / len(y)
    return [mean_x, mean_y]

def animate(loc1, loc2):
    # Draw x and y lists
    ax.clear()
    ax1.clear()
    ax.scatter(loc1[0],loc1[1])
    ax.set_title('Mobile 1')
    ax.set_xlabel('x axis')
    ax.set_ylabel('y axis')
    ax.set_xlim([0,8])
    ax.set_ylim([0,4])
    ax1.scatter(loc2[0],loc2[1])

    # Format plot

    ax1.set_title('Mobile 2')
    ax1.set_xlabel('x axis')
    ax1.set_ylabel('y axis')
    ax1.set_xlim([0,8])
    ax1.set_ylim([0,4])
    plt.show()
    plt.pause(0.5)
    plt.close()

def listToString(s): 
    
    # initialize an empty string
    str1 = "" 
    
    # traverse in the string  
    for ele in s: 
        str1 += ele  
    
    # return string  
    return str1 

def Read():
    model = get_trainingmodel()
    temp2 = list()
    temp_k1 = list()
    temp_m1 = list()
    temp_combine1 = list()
    temp_k2 = list()
    temp_m2 = list()
    temp_combine2 = list()
    retrived = my_device.find({'variable':['rssi1','rssi2','ultrasonic'],'query':'last_value'})
    for d in retrived['result']:
        temp2.append(d['value'])
    retrived_parsed1 = [int(s) for s in temp2[0].split(',')]
    retrived_parsed2 = [int(s) for s in temp2[1].split(',')]
    retrived_parsed3 = [int(s) for s in temp2[2].split(',')] ## ultrasonic value
    temp2 = []
    predicted_m1 = model.predict([retrived_parsed1]) ## mobile1 value here
    predicted_m2 = model.predict([retrived_parsed2]) ## mobile2 value here
    valid_x_m1 = []
    valid_y_m1 = []
    valid_rad_m1 = []
    valid_x_m2 = []
    valid_y_m2 = []
    valid_rad_m2 = []

    rssi_dists_m1 = []
    rssi_dists_m2 = []

    us_vals = [retrived_parsed3[0] / 35,
                retrived_parsed3[1] / 35,
                retrived_parsed3[2] / 35,
                retrived_parsed3[3] / 35]

    for i in retrived_parsed1:
        rssi_dists_m1.append(i)

    for i in retrived_parsed2:
        rssi_dists_m2.append(i)

    for j in range(NUM_STATIC_NODES):
        # Check RSSI ranges
        if rssi_dists_m1[j] == -128 or rssi_dists_m1[j] >= 0:
            # Dodgy RSSI reading, just skip this one
            continue
        else:
            valid_x_m1.append(X_BEACONS[j])
            valid_y_m1.append(Y_BEACONS[j])
            valid_rad_m1.append(10 ** ((-58 - rssi_dists_m1[j]) / 30))

    for j in range(NUM_STATIC_NODES):
        # Check RSSI ranges
        if rssi_dists_m2[j] == -128 or rssi_dists_m2[j] >= 0:
            # Dodgy RSSI reading, just skip this one
            continue
        else:
            valid_x_m2.append(X_BEACONS[j])
            valid_y_m2.append(Y_BEACONS[j])
            valid_rad_m2.append(10 ** ((-58 - rssi_dists_m2[j]) / 30))

    for k in range(4):
        if us_vals[k] < 1.5:
            valid_x_m1.append(US_X_BEACONS[k])
            valid_x_m2.append(US_X_BEACONS[k])
            valid_y_m1.append(US_Y_BEACONS[k])
            valid_y_m2.append(US_Y_BEACONS[k])
            valid_rad_m1.append(us_vals[k])
            valid_rad_m2.append(us_vals[k])

    valid_x_glob_m1 = valid_x_m1.copy()
    valid_y_glob_m1 = valid_y_m1.copy()
    valid_x_glob_m2 = valid_x_m2.copy()
    valid_y_glob_m2 = valid_y_m2.copy()
    valid_rad_glob_m1 = valid_rad_m1.copy()
    valid_rad_glob_m2 = valid_rad_m2.copy()

    x_rand_m1 = np.random.rand(1)
    y_rand_m1 = np.random.rand(1)
    x_rand_m2 = np.random.rand(1)
    y_rand_m2 = np.random.rand(1)

    start_m1 = (x_rand_m1, y_rand_m1)
    start_m2 = (x_rand_m2, y_rand_m2)

    endpos_m1 = opt.fmin_powell(minimise_m1, start_m1, disp=False)
    endpos_m2 = opt.fmin_powell(minimise_m2, start_m2, disp=False)

    count = 0
    while count < 3:
        temp_m2.append(endpos_m2)
        temp_k2.append(predicted_m2[0])
        temp_m1.append(endpos_m1)
        temp_k1.append(predicted_m1[0])
        count += 1

    temp_combine1 = temp_k1 + temp_m2
    temp_combine2 = temp_k2 + temp_m1
    # print(temp_combine1)
    # print(temp_combine2)
    loc1 = Kalman(temp_combine1)
    loc2 = Kalman(temp_combine2)
    # animate(loc1,loc2)
    m1_x =  round(loc1[0], significant_digits - int(math.floor(math.log10(abs(loc1[0])))) - 1)
    m1_y =  round(loc1[1], significant_digits - int(math.floor(math.log10(abs(loc1[1])))) - 1)
    m2_x =  round(loc2[0], significant_digits - int(math.floor(math.log10(abs(loc2[0])))) - 1)
    m2_y =  round(loc2[1], significant_digits - int(math.floor(math.log10(abs(loc2[1])))) - 1)
    print("Mobile 1:")
    print(loc1)
    print("Mobile 2:")
    print(loc2)
    mobile1x_var.set(m1_x)
    mobile1y_var.set(m1_y)
    mobile2x_var.set(m2_x)
    mobile2y_var.set(m2_y)
    main_window.after(200, Read)
    time.sleep(0.01)
    return

Read()
accel_label = Label(centre_seg1, font=("Georgia", 12), text="Mobile location: (x,y)")
accel_label.grid(column=0, columnspan=2, row=0, padx=20, pady=20)
r_node1 = Label(centre_seg1, font=("Georgia", 8), text="Mobile1: ")
r_node2 = Label(centre_seg1, font=("Georgia", 8), text="Mobile2: ")
r_node1.grid(column=0, row=1, padx=10, pady=10)
r_node2.grid(column=0, row=2, padx=10, pady=10)
r1_reading = Label(centre_seg1, font=("Georgia", 8), text="Undetected", textvariable=mobile1x_var)
r2_reading = Label(centre_seg1, font=("Georgia", 8), text="Undetected", textvariable=mobile1y_var)
r3_reading = Label(centre_seg1, font=("Georgia", 8), text="Undetected", textvariable=mobile2x_var)
r4_reading = Label(centre_seg1, font=("Georgia", 8), text="Undetected", textvariable=mobile2y_var)
r1_reading.grid(column=1, row=1, padx=10, pady=10)
r2_reading.grid(column=2, row=1, padx=10, pady=10)
r3_reading.grid(column=1, row=2, padx=10, pady=10)
r4_reading.grid(column=2, row=2, padx=10, pady=10)
main_window.mainloop()

# if __name__ == "__main__":
#     model = get_trainingmodel()

#     temp_k1 = list()
#     temp_m1 = list()
#     temp_combine1 = list()
#     temp_k2 = list()
#     temp_m2 = list()
#     temp_combine2 = list()
#     while True:
#         retrived = my_device.find({'variable':['rssi1','rssi2','ultrasonic'],'query':'last_value'})
#         for d in retrived['result']:
#             temp2.append(d['value'])
#         retrived_parsed1 = [int(s) for s in temp2[0].split(',')]
#         retrived_parsed2 = [int(s) for s in temp2[1].split(',')]
#         retrived_parsed3 = [int(s) for s in temp2[2].split(',')] ## ultrasonic value
#         temp2 = []
#         predicted_m1 = model.predict([retrived_parsed1]) ## mobile1 value here
#         predicted_m2 = model.predict([retrived_parsed2]) ## mobile2 value here

#         # valid_x_m1 = []
#         # valid_y_m1 = []
#         # valid_rad_m1 = []
#         # valid_x_m2 = []
#         # valid_y_m2 = []
#         # valid_rad_m2 = []

#         # rssi_dists_m1 = []
#         # rssi_dists_m2 = []

#         # us_vals = [retrived_parsed3[0] / 35,
#         #            retrived_parsed3[1] / 35,
#         #            retrived_parsed3[2] / 35,
#         #            retrived_parsed3[3] / 35]

#         # for i in retrived_parsed1:
#         #     rssi_dists_m1.append(i)

#         # for i in retrived_parsed2:
#         #     rssi_dists_m2.append(i)

#         # for j in range(NUM_STATIC_NODES):
#         #     # Check RSSI ranges
#         #     if rssi_dists_m1[j] == -128 or rssi_dists_m1[j] >= 0:
#         #         # Dodgy RSSI reading, just skip this one
#         #         continue
#         #     else:
#         #         valid_x_m1.append(X_BEACONS[j])
#         #         valid_y_m1.append(Y_BEACONS[j])
#         #         valid_rad_m1.append(10 ** ((-58 - rssi_dists_m1[j]) / 30))

#         # for j in range(NUM_STATIC_NODES):
#         #     # Check RSSI ranges
#         #     if rssi_dists_m2[j] == -128 or rssi_dists_m2[j] >= 0:
#         #         # Dodgy RSSI reading, just skip this one
#         #         continue
#         #     else:
#         #         valid_x_m2.append(X_BEACONS[j])
#         #         valid_y_m2.append(Y_BEACONS[j])
#         #         valid_rad_m2.append(10 ** ((-58 - rssi_dists_m2[j]) / 30))

#         # for k in range(4):
#         #     if us_vals[k] < 1.5:
#         #         valid_x_m1.append(US_X_BEACONS[k])
#         #         valid_x_m2.append(US_X_BEACONS[k])
#         #         valid_y_m1.append(US_Y_BEACONS[k])
#         #         valid_y_m2.append(US_Y_BEACONS[k])
#         #         valid_rad_m1.append(us_vals[k])
#         #         valid_rad_m2.append(us_vals[k])

#         # valid_x_glob_m1 = valid_x_m1.copy()
#         # valid_y_glob_m1 = valid_y_m1.copy()
#         # valid_x_glob_m2 = valid_x_m2.copy()
#         # valid_y_glob_m2 = valid_y_m2.copy()
#         # valid_rad_glob_m1 = valid_rad_m1.copy()
#         # valid_rad_glob_m2 = valid_rad_m2.copy()

#         # x_rand_m1 = np.random.rand(1)
#         # y_rand_m1 = np.random.rand(1)
#         # x_rand_m2 = np.random.rand(1)
#         # y_rand_m2 = np.random.rand(1)

#         # start_m1 = (x_rand_m1, y_rand_m1)
#         # start_m2 = (x_rand_m2, y_rand_m2)

#         # endpos_m1 = opt.fmin_powell(minimise_m1, start_m1, disp=False)
#         # endpos_m2 = opt.fmin_powell(minimise_m2, start_m2, disp=False)

#         if (len(temp_k1) > 3):
#             temp_combine1 = temp_k1
#             temp_combine2 = temp_k2 
#             # print(temp_combine1)
#             # print(temp_combine2)
#             loc1 = Kalman(temp_combine1)
#             loc2 = Kalman(temp_combine2)
#             # animate(loc1,loc2)
#             print("Mobile 1:")
#             print(loc1)
#             print("Mobile 2:")
#             print(loc2)
#             temp_k1 = []
#             temp_m1 = []
#             temp_k2 = []
#             temp_m2 = []
#             temp_combine1 = []
#             temp_combine2 = []
#         # temp_m2.append(endpos_m2)
#         temp_k2.append(predicted_m2[0])
#         # temp_m1.append(endpos_m1)
#         temp_k1.append(predicted_m1[0])


