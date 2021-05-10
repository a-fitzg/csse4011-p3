import tago

MY_DEVICE_TOKEN = '3503290b-05e5-433d-a864-e1b8e7bfbf11'
my_device = tago.Device(MY_DEVICE_TOKEN)

array_value = [1223, 469, 45]

data_to_insert = {
  'variable': 'rssi',
  'value': array_value
}

# my_device.insert(data_to_insert)  # Without response

result = my_device.insert(data_to_insert)  # With response
if result['status']:
  print(result['result'])
else:
  print(result['message'])
