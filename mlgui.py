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
T = [-61,-70,-59,-69,-66,-64,-55,-66]

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
predicted= model.predict([T]) 
print(predicted)


# for l in findloc['result']:
#   raw_loc = l['value']
  
# loc_n = [int(s) for s in raw_loc.split(',')]

# count_x = 0
# count_y = 0

# for x in r_n:
#   if count_x < ITERATE_X:
#     temp_x.append(x)
#     count_x += 1
#   else:
#     X_train.append(temp_x)
#     temp_x = []
#     count_x = 0

# for y in loc_n:
#   if count_y < ITERATE_Y:
#     temp_y.append(y)
#     count_y += 1
#   else:
#     Y_train.append(temp_y)
#     temp_y = []
#     count_y = 0

# print(len(X_train))
# print(len(Y_train))