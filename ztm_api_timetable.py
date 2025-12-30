import requests
from datetime import datetime

with open("api-um-apikey", "r") as file:
    apikey = file.read().strip()


config = {"stops": {
            "Czynszowa": {"busstopNr": "01", "busstopId" : 1069, "lines": [23], "direction_blacklist": ["Czynszowa"]},
            "Rzeszotarskiej": {"busstopNr": "01", "busstopId" : 1052, "lines": [190, 120], "direction_blacklist": []},
            }
         }

def download_timetable(config):

    try:

        timetable = []
        for stop_name, stop_data in config["stops"].items():
            for line in stop_data["lines"]:
                response = requests.get(
                    f"https://api.um.warszawa.pl/api/action/dbtimetable_get?id=e923fa0e-d96c-43f9-ae6e-60518c9f3238&busstopId={stop_data["busstopId"]}&busstopNr={stop_data["busstopNr"]}&line={line}&apikey={apikey}"
                )
                for record in response.json()["result"]:
                    stop_time, direction = (None, None)
                    for dict in record:
                        if dict["key"] == 'czas':
                            stop_time = [int(part) for part in dict["value"].split(":")]
                            stop_time = 60*stop_time[0] + stop_time[1]
                        elif dict["key"] == 'kierunek':
                            direction = dict["value"]
                    if direction not in stop_data["direction_blacklist"]:
                        timetable.append({"line": line, "direction": direction, "stop_time": stop_time, "stop_name": stop_name})

        timetable.sort(key=lambda x: x["stop_time"])
        
        return timetable
    
    except Exception as e:
        print(f"Could not update timetable: {e}")

def get_departures_string(timetable, time, n=8):
    upcoming_departures = []
    for record in timetable:
        if time > record["stop_time"]:
            continue
        upcoming_departures.append(record)
        if len(upcoming_departures) > n:
            break
    result = ""
    for record in upcoming_departures:
        result += f"{record["line"]:<6}{record["direction"]:<24}{record["stop_time"] - time} min\n"
    return result
