from apscheduler.schedulers.background import BackgroundScheduler
import random
from flask_app.socketio_events.bbbw import bbbwSessionInfo_updateVolumeLevel, bbbwMiscellanous_updateRoomState
from flask_app import app
from datetime import datetime, timezone
from flask_app.database.crud import update_instrument_wear_values

scheduler = BackgroundScheduler()
def core_per_second():
    with app.app_context():
        update_instrument_wear_values()
        current_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M')
        simulated_volume_level = random.randint(0, 30)
        data = {'volume_level': simulated_volume_level, 'time_stamp': current_time}
        # Simulates a socketio event emitted from bbbw_SessionInfo
        bbbwSessionInfo_updateVolumeLevel(data)

scheduler.add_job(core_per_second, 'cron', second='*')
scheduler.start()
