import tago
from sklearn.neighbors import KNeighborsClassifier   

MY_DEVICE_TOKEN = '3503290b-05e5-433d-a864-e1b8e7bfbf11'
my_device = tago.Device(MY_DEVICE_TOKEN)

temp2 = []

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
    predicted_m1= model.predict([retrived_parsed1]) ## mobile1 value here
    predicted_m2= model.predict([retrived_parsed2]) ## mobile2 value here
    print(predicted_m1[0])
    print(predicted_m2[0])
    print(retrived_parsed3)

