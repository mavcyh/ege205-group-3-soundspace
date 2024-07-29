from apscheduler.schedulers.background import BackgroundScheduler
import random
from flask_app.socketio_events.bbbw import bbbwSessionInfo_updateVolumeLevel, bbbwMiscellanous_updateRoomState
from flask_app import app
from datetime import datetime, timezone
from flask_app.database.crud import update_instrument_wear_values, get_session_active_core

scheduler = BackgroundScheduler()

session_active = False  # Global variable to keep track of session state

def check_session():
    global session_active
    with app.app_context():
        start_datetime, end_datetime = get_session_active_core()
        if end_datetime:
            current_time = datetime.now(timezone.utc)
            if current_time < end_datetime:
                session_active = True
                remaining_time_seconds = (end_datetime - current_time).total_seconds()
                remaining_time_seconds = int(remaining_time_seconds)
                print(f"Remaning time (seconds): {remaining_time_seconds}")
            else:
                session_active = False
        else:
            session_active = False
        
        print(f"Session active: {session_active}")

def core_per_second():
    with app.app_context():
        update_instrument_wear_values()
        event_time_stamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M')
        simulated_volume_level = random.randint(0, 30)
        data = {'volume_level': simulated_volume_level, 'time_stamp': event_time_stamp}
        # Simulates a socketio event emitted from bbbw_SessionInfo
        bbbwSessionInfo_updateVolumeLevel(data)

# Schedule check_session to run every minute
scheduler.add_job(check_session, 'cron', minute='*')

# Schedule core_per_second to run every second
scheduler.add_job(core_per_second, 'cron', second='*')

scheduler.start()

# check_session()
