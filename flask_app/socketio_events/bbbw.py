from flask import request
from flask_app import socketio
from flask_app.database.crud import *
from datetime import datetime, timezone

roomData = {
    "room_door_status": None,
    "instrument_data": [],
    "loitering_detected": False, 
    "item_dropped": False
}

def update_room_data():
    roomData["instrument_data"] = get_instrument_data()
    
#region SOCKETIO EVENTS

#region bbbwRoomDoor
@socketio.event
def bbbwRoomDoor_DoorState(data):
    if data["door_state"] == "OPENED":
        roomData["room_door_status"] = "OPENED"

    elif data["door_state"] == "CLOSED":
        roomData["room_door_status"] = "CLOSED"

    elif data["door_state"] == "BROKEN INTO":
        roomData["room_door_status"] = "BROKEN INTO"
        event = "door_broken_into"
        update_event(event, "Door Broken into!", 2) # event, event name, severity
    print(f"DOOR {data['door_state']}")
    
#endregion bbbwRoomDoor


#region bbbwInstrumentLocker

instrument_missing_trip = []
@socketio.event
def bbbwInstrumentLocker_Usage(data):
    global instrument_missing_trip
    for index, instrument in enumerate(roomData["instrument_data"]):
        if instrument["locker_id"] == data["locker_id"]:
            roomData["instrument_data"][index]["usage"] = data["usage"]
            return
    start_datetime, end_datetime = get_session_active()
    if data["usage"] and not end_datetime:
        instrument_missing_trip.append(data["locker_id"])
        
#endregion bbbwInstrumentLocker


#region bbbwSessionInfo

@socketio.event
def bbbwSessionInfo_updateVolumeLevel(data):
    if data["volume_level"] >= 10:
        socketio.emit("serverToSessionInfo_maximumVolumeExceeded", {})
    write_volume_level_data(data["volume_level"])
    print(f"Volume level: {data["volume_level"]}")

#endregion bbbwSessionInfo


#region bbbwMiscellanous

loitering_detected_trip = False
@socketio.event
def bbbwMiscellanous_updateRoomState(data):
    global loitering_detected_trip
    insert_humidity_data(data["humidity_level"])
    if data["motion_detected"] == True:
        loitering_detected_trip = True
        start_datetime, end_datetime = get_session_active()
        if start_datetime and end_datetime:
            roomData["loitering_detected"] = False
        elif start_datetime is None and end_datetime is None:
            roomData["loitering_detected"] = True

    if data["humidity_level"] >= 75:
        event = "high_humidity"
        update_event(event, "Humidity Level Exceeded!", 0)

@socketio.event
def bbbwMiscellanous_deviceDropped():
    event = "dropped"
    update_event(event, "Device Dropped!", 2)
    roomData["item_dropped"] = True

#endregion bbbwMiscellanous

#endregion SOCKETIO EVENTS

#region START/ END SESSION


connected_bbbw_session_id = {
    "RoomDoor": "",
    "InstrumentLocker": {},
    "SessionInfo": "",
    "Miscellanous": "",
}


@socketio.event
def bbbw_connected(data):
    # Adds session id of connected BBBW to connected_bbbw_session_id.
    # For instrument lockers, there can be multiple and there is an extra key "intrument_locker_number".
    bbbw_role = data["bbbw_role"]
    if bbbw_role == "InstrumentLocker":
        connected_bbbw_session_id["InstrumentLocker"][data["instrument_locker_number"]] = str(request.sid)
        print(f"bbbwInstrumentLocker {data["instrument_locker_number"]} CONNECTED")
    else:
        connected_bbbw_session_id[data["bbbw_role"]] = str(request.sid)
        print(f"bbbw{bbbw_role} CONNECTED")
        
    # Emit SocketIO event based on device connected
    match bbbw_role:
        case "RoomDoor":
            temp_password = update_temporary_password()
            TxData = {
                "temporary_password": temp_password,
            }
            socketio.emit("serverToRoomDoor_updateTemporaryPassword", TxData)
            
        case "InstrumentLocker":
            vol_limit = get_volume_limit()
            start_datetime, end_datetime = get_session_active_core()
            if end_datetime:
                current_time = datetime.now(timezone.utc)
                remaining_time_seconds = int((end_datetime - current_time).total_seconds())
            else:
                remaining_time_seconds = None
            TxData = get_all_instrument_names()
            socketio.emit("serverToInstrumentLocker_connected", TxData)
            TxData = {"unlocked_locker_ids": get_booked_lockers(),
                      "session_duration": remaining_time_seconds}
            socketio.emit("serverToInstrumentLocker_updateLockers", TxData)
            
        case "SessionInfo":
            vol_limit = get_volume_limit()
            start_datetime, end_datetime = get_session_active_core()
            if end_datetime:
                current_time = datetime.now(timezone.utc)
                remaining_time_seconds = int((end_datetime - current_time).total_seconds())
            else:
                remaining_time_seconds = None
            TxData = {
                "session_duration_left": remaining_time_seconds,
                "maximum_volume_level": vol_limit,
            }
            socketio.emit("serverToSessionInfo_connected", TxData)
            
        case "Miscellanous":
            start_datetime, end_datetime = get_session_active()
            TxData = {
                "session_active": True if end_datetime else False,
            }
            socketio.emit("serverToMiscellanous_connected", TxData)

@socketio.event
def disconnect():
    session_id = str(request.sid)
    for bbbw_role in connected_bbbw_session_id:
        if connected_bbbw_session_id[bbbw_role] == session_id:
            connected_bbbw_session_id[bbbw_role] = ""
            print(f"bbbw{bbbw_role} DISCONNECTED")
            return
    for instrument_locker_number in connected_bbbw_session_id["InstrumentLocker"].keys():
        if connected_bbbw_session_id["InstrumentLocker"][instrument_locker_number] == session_id:
            connected_bbbw_session_id["InstrumentLocker"][instrument_locker_number] = ""
            print(f"bbbwInstrumentLocker {instrument_locker_number} DISCONNECTED")
            return

#endregion START/ END SESSION