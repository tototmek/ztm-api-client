import requests
print(requests.get("http://localhost:21370/departures/8").json()["message"], end="")