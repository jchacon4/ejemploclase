import requests

data = '{"who":"Juan"}'
response = requests.patch('https://caraudem.firebaseio.com/.json', data=data)
