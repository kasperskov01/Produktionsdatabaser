import requests
import json

query = {'username':'Kasper', 'password':'123', 'user_type':'chef'}
response = requests.post('https://proddb.herokuapp.com/api/user/signup', json=query)
data = response.json()
if data:
    print(data)
    print(data["user_exists"])