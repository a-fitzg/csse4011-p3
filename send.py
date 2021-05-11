import tago

MY_DEVICE_TOKEN = '3503290b-05e5-433d-a864-e1b8e7bfbf11'
my_device = tago.Device(MY_DEVICE_TOKEN)
x  = 1
y  = 2


while True:
    lis = [x,y]

    data = {
        'variable': 'testdata',
        'value': lis
    }
    my_device.insert(data)
    x += 1
    y += 1
    