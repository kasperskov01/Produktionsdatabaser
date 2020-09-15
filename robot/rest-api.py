import requests
import json

query = {'username':'Kasper', 'password':'123'}
response = requests.post('https://proddb.herokuapp.com/api/user/login', params=query)
data = response.content
print(data)