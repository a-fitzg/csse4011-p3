import tago
from sklearn.neighbors import KNeighborsClassifier   

MY_DEVICE_TOKEN = '3503290b-05e5-433d-a864-e1b8e7bfbf11'
my_device = tago.Device(MY_DEVICE_TOKEN)

ITERATE_X = 8
ITERATE_Y = 10
X_train = []
Y_train = []
temp_x = []
temp_y = []
count = 0
findData = my_device.find({'variable':'trainingset'})
T = [-74,-65,-65,-65,-78,-67,-63,-60
]

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

## Retrive data from dashboard after this line

predicted= model.predict([T]) ## RSSI value here
print(predicted[0])
