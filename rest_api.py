import requests
import json

def robot_order_get():
    #query = {'username':'Kasper', 'password':'123', 'user_type':'chef'}
    response = requests.get('https://proddb.herokuapp.com/api/robot/order/get')
    try:
        data = response.json()
        print(data)
        print(data["order"])
        return data
    except:
        print("Tobias")

def robot_order_status_set(order_id, status):
    query = {'order_id':order_id, 'status':status}
    response = requests.post('https://proddb.herokuapp.com/api/robot/order/status/set', json=query)
    try:
        data = response.json()
        print(data)
        print(data["update_status"])
        return data
    except:
        print("Tobias")
    