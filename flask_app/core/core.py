from apscheduler.schedulers.background import BackgroundScheduler
from flask_app.socketio_events.bbbw import update_room_data
from flask_app import app, socketio
from datetime import datetime, timezone
from flask_app.database.crud import get_session_active_core, update_event, update_temporary_password, get_volume_limit, get_booked_lockers, update_instrument_wear_values
from flask_app.socketio_events.bbbw import loitering_detected_trip, instrument_missing_trip, roomData

scheduler = BackgroundScheduler()

def core_per_two_minutes():
    global loitering_detected_trip, instrument_missing_trip
    loitering_detected_trip = False
    instrument_missing_trip = []
    with app.app_context():
        event = "wear_exceeded"
        update_event(event, "", None)

def core_per_minute():
    print("CORE PER MINUTE:")
    with app.app_context():
        update_instrument_wear_values(roomData)
        print("Wear values of instruments updated.")
        
        # bbbwRoomDoor
        temp_password = update_temporary_password()
        TxData = {
            "temporary_password": temp_password,
        }
        socketio.emit("serverToRoomDoor_updateTemporaryPassword", TxData)
        print(f"Updated temporary password: {temp_password}")
        
        # bbbwSessionInfo & bbbwMiscellanous
        current_volume_limit = get_volume_limit()
        vol_limit = {"maximum_volume_level": current_volume_limit}
        socketio.emit("serverToSessionInfo_updateMaximumVolumeLevel", vol_limit)
        unlocked_lockers = get_booked_lockers()
        start_datetime, end_datetime = get_session_active_core()
        if end_datetime:
            current_time = datetime.now(timezone.utc)
            remaining_time_seconds = int((end_datetime - current_time).total_seconds())
            TxData = {"unlocked_locker_ids": unlocked_lockers,
                      "session_duration": remaining_time_seconds}
            socketio.emit("serverToInstrumentLocker_updateLockers", TxData)
            socketio.emit("serverToSessionInfo_updateSession", {"session_duration": remaining_time_seconds})
            socketio.emit("serverToMiscellanous_connected", {"session_active": True})
            print(f"Remaining session duration: {remaining_time_seconds}s")
            print(f"Unlocked lockers {TxData["unlocked_locker_ids"]}.")
        else:
            TxData = {"unlocked_locker_ids": [],
                      "session_duration": None}
            socketio.emit("serverToInstrumentLocker_updateLockers", TxData)
            socketio.emit("serverToMiscellanous_connected", {"session_active": False})
            print(f"No session active.")
        update_room_data()
        print("END OF CORE PER MINUTE")
            

scheduler.add_job(core_per_minute, 'cron', minute='*')

scheduler.add_job(core_per_two_minutes, 'cron', minute='*/2')

scheduler.start()