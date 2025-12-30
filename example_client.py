import requests
print(requests.get("http://192.168.0.6:21370/departures/8").json()["message"], end="")