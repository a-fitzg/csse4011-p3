import tago
import numpy as np
import scipy.optimize as opt
from sklearn.neighbors import KNeighborsClassifier   

MY_DEVICE_TOKEN = '3503290b-05e5-433d-a864-e1b8e7bfbf11'
my_device = tago.Device(MY_DEVICE_TOKEN)

GRID_X_SIZE = 8
GRID_Y_SIZE = 4

NUM_STATIC_NODES = 8

X_BEACONS = [0, GRID_X_SIZE, GRID_X_SIZE / 3, 2 * GRID_X_SIZE / 3,
             GRID_X_SIZE, 0, GRID_X_SIZE / 3, 2 * GRID_X_SIZE / 3]
Y_BEACONS = [GRID_Y_SIZE, GRID_Y_SIZE, 0, 0,
             0, 0, GRID_Y_SIZE, GRID_Y_SIZE]

valid_x_glob_m1 = []
valid_y_glob_m1 = []
valid_rad_glob_m1 = []
valid_x_glob_m2 = []
valid_y_glob_m2 = []
valid_rad_glob_m2 = []

temp2 = []


def calc_distance_m1(point):
    points = np.array([valid_x_glob_m1, valid_y_glob_m1]).T
    diffs = np.subtract(points, point)
    sum_powers = np.sum(np.power(diffs, 2), axis=1)
    root_sum = np.power(sum_powers, 0.5)
    diff2 = np.subtract(root_sum, valid_rad_glob_m1)
    return diff2


def minimise_m1(point):
    dist = calc_distance_m1(point)
    err = np.linalg.norm(dist / valid_rad_glob_m1)
    return err


def calc_distance_m2(point):
    points = np.array([valid_x_glob_m2, valid_y_glob_m2]).T
    diffs = np.subtract(points, point)
    sum_powers = np.sum(np.power(diffs, 2), axis=1)
    root_sum = np.power(sum_powers, 0.5)
    diff2 = np.subtract(root_sum, valid_rad_glob_m2)
    return diff2


def minimise_m2(point):
    dist = calc_distance_m2(point)
    err = np.linalg.norm(dist / valid_rad_glob_m2)
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


if __name__ == "__main__":
    model = get_trainingmodel()
    while True:
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

        endpos_m1 = opt.fmin_powell(minimise_m1, start_m1)
        endpos_m2 = opt.fmin_powell(minimise_m2, start_m2)

        print(f"NODE 1 LOCATION: ({endpos_m1[0]}, {endpos_m1[1]})")
        print(f"NODE 2 LOCATION: ({endpos_m2[0]}, {endpos_m2[1]})")

        print(predicted_m1[0])
        print(predicted_m2[0])
        print(retrived_parsed3)
