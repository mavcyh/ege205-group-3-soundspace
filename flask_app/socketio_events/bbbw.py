from flask import request
from flask_app import socketio
from flask_app.database.crud import write_volume_level_data, update_event, insert_humidity_data, get_instrument_data, get_session_active

roomData = {
    "room_door_status": 'CLOSED',
    "instrument_data": [{'locker_id': '1', 'instrument_name': 'Fender Stratocaster', 'wear_value': 50, 'price_per_hour': 2.5, 'usage': False},
                      {'locker_id': '2', 'instrument_name': 'Ibanez SR300E', 'wear_value': 70, 'price_per_hour': 1.5, 'usage': False}],
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
        roomData["room_door_status"] == "BROKEN INTO"
        event = "door broken into"
        update_event(event)

#endregion bbbwRoomDoor
@socketio.event
def change_master_password(master_password):
    TxData = {
    "master_password": master_password,
    "temporary_password": "123412",
    }
    socketio.emit("serverToRoomDoor_updatePasswords ", TxData)
#region bbbwInstrumentLocker

#endregion bbbwInstrumentLocker

#region bbbwSessionInfo
@socketio.event
def bbbwSessionInfo_updateVolumeLevel(data):
    if data["volume_level"] >= 10:
        TxData = {}
        socketio.emit("serverToSessionInfo_maximumVolumeExceeded", TxData)
    write_volume_level_data(data["time_stamp"],[data["volume_level"]], 10)

#endregion bbbwSessionInfo

#region bbbwMiscellanous

@socketio.event
def bbbwMiscellanous_updateRoomState(data):
    print(f"Humidity Level: {data["humidity_level"]}%")
    print("Motion Detected" if data["motion_detected"] else "Motion Not Detected")
    insert_humidity_data(data["humidity_level"])
    if data["motion_detected"] == True:
        event = "motion"
        update_event(event)
        start_datetime, end_datetime = get_session_active()
        if start_datetime and end_datetime:
            roomData["loitering_detected"] = False
        elif start_datetime is None and end_datetime is None:
            roomData["loitering_detected"] = True

@socketio.event
def bbbwMiscellanous_deviceDropped():
    event = "dropped"
    update_event(event)
    start_datetime, end_datetime = get_session_active()
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
    pack_up_duration = 30
    leave_duration = 30
    match bbbw_role:
        case "RoomDoor":
            TxData = {
                "master_password": "111111",
                "temporary_password": "123412",
            }
            socketio.emit("serverToRoomDoor_updatePasswords ", TxData)
            
        case "InstrumentLocker":
            TxData = {
                data["instrument_locker_number"]: {
                    "pack_up_duration": pack_up_duration,
                    "leave_duration": leave_duration,
                    "session_duration_left": None,
                    "locker_locked": False,
                    "instrument_name": "Fender Bass"
                }
            }
            socketio.emit("serverToInstrumentLocker_connected", TxData)
        
        case "SessionInfo":
            TxData = {
                "pack_up_duration": pack_up_duration,
                "leave_duration": leave_duration,
                "session_duration_left": None,
                "maximum_volume_level": 10,
            }
            socketio.emit("serverToSessionInfo_connected", TxData)
            
        case "Miscellanous":
            TxData = {
                "session_active": True,
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