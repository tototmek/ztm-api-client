from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import uvicorn
from ztm_api_timetable import download_timetable, get_departures_string, load_config

app = FastAPI()

config = load_config("config.yaml")
timetable = download_timetable(config)
status = "ok"

def update_function():
    print(f"Updating timetable")
    global timetable
    global status
    try:
        timetable = download_timetable(config)
        status = "ok"
    except Exception as e:
        print(f"Couldn't update timetable: {e}")
        status = "ztm api error"

scheduler = BackgroundScheduler()
scheduler.add_job(update_function, 'cron', hour=1, minute=30)
scheduler.start()


@app.get("/departures/{n}")
async def generate_string(n: int):
    current_time = datetime.now()
    current_time = current_time.hour * 60 + current_time.minute
    return {"message": get_departures_string(timetable, current_time, n, config), "status": status}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=config["port"])