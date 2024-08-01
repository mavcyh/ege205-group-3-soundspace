from apscheduler.schedulers.background import BackgroundScheduler
import random
from flask_app.socketio_events.bbbw import bbbwSessionInfo_updateVolumeLevel, bbbwMiscellanous_updateRoomState, update_room_data, change_temporary_password
from flask_app import app, socketio
from datetime import datetime, timezone
from flask_app.database.crud import update_instrument_wear_values, get_session_active_core, update_event, update_temporary_password, get_volume_limit

scheduler = BackgroundScheduler()

session_active = False  # Global variable to keep track of session state

volume_limit = {
    "00:00": 5,
    "07:00": 7,
    "10:00": 8,
    "14:00": 9,
    "20:00": 6,
}

def check_session():
    global session_active
    with app.app_context():
        current_volume_limit = get_volume_limit(volume_limit)
        vol_limit = {"maximum_volume_level": current_volume_limit}
        socketio.emit("serverToSessionInfo_updateMaximumVolumeLevel", vol_limit)
        start_datetime, end_datetime = get_session_active_core()
        if end_datetime:
            current_time = datetime.now(timezone.utc)
            if current_time < end_datetime:
                session_active = True
                remaining_time_seconds = int((end_datetime - current_time).total_seconds())
                TxData = {"session_duration": remaining_time_seconds}
                socketio.emit("serverToSessionInfo_updateSession", TxData)
                print(f"Remaning time (seconds): {remaining_time_seconds}")
            else:
                session_active = False
        else:
            session_active = False

def check_wear_exceeded():
    with app.app_context():
        update_event("wear_exceeded")

def core_per_second():
    with app.app_context():
        global simulated_humidity_level

        start_datetime, end_datetime = get_session_active_core()
        session_status = True if start_datetime and end_datetime else False
        socketio.emit("serverToMiscellanous_connected", {"session_active": session_status})

        update_instrument_wear_values()   
        TxData = {
            "humidity_level": random.randint(50, 60),
            "motion_detected": False
        }   
        bbbwMiscellanous_updateRoomState(TxData)

        event_time_stamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M')
        simulated_volume_level = random.randint(0, 30)
        data = {'volume_level': simulated_volume_level, 'time_stamp': event_time_stamp}
        # Simulates a socketio event emitted from bbbw_SessionInfo
        bbbwSessionInfo_updateVolumeLevel(data)

        update_room_data()
        temp_password = update_temporary_password() 
        change_temporary_password(temp_password)

# Schedule check_session to run every minute
scheduler.add_job(check_session, 'cron', minute='*')

# Check if the wear_value has exceeded every 30 minutes
scheduler.add_job(check_wear_exceeded, 'cron', minute='*/30')

# Schedule core_per_second to run every second
scheduler.add_job(core_per_second, 'cron', second='*')

scheduler.start()

# check_session()
