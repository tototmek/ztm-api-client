from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import uvicorn
from ztm_api_timetable import download_timetable, get_departures_string, config

app = FastAPI()

timetable = download_timetable(config)

def update_function():
    print(f"Updating timetable")
    global timetable
    timetable = download_timetable(config)

scheduler = BackgroundScheduler()
scheduler.add_job(update_function, 'cron', hour=1, minute=30)
scheduler.start()


@app.get("/departures_string")
async def generate_string():
    current_time = datetime.now()
    current_time = current_time.hour * 60 + current_time.minute
    return {"message": get_departures_string(timetable, current_time, 8)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=21370)