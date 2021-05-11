import tago

MY_DEVICE_TOKEN = '3503290b-05e5-433d-a864-e1b8e7bfbf11'
my_device = tago.Device(MY_DEVICE_TOKEN)

while True:
    data = my_device.find({'variable':'testdata','qty':'last_value'})
    for d in data['result']:
        temp = d['value']
    print(temp)