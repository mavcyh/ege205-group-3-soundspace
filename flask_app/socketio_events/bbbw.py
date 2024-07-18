from flask import request
from flask_app import socketio

#region SOCKETIO EVENTS

#region bbbwRoomDoor

#endregion bbbwRoomDoor

#region bbbwInstrumentLocker

#endregion bbbwInstrumentLocker

#region bbbwSessionInfo

@socketio.event
def bbbwSessionInfo_updateVolumeLevel(data):
    if data["volume_level"] >= 10:
        TxData = {}
        socketio.emit("serverToSessionInfo_maximumVolumeExceeded", TxData)

#endregion bbbwSessionInfo

#region bbbwMiscellanous

@socketio.event
def bbbwMiscellanous_updateRoomState(data):
    print(f"Humidity Level: {data["humidity_level"]}%")
    print("Motion Detected" if data["motion_detected"] else "Motion Not Detected")

@socketio.event
def bbbwMiscellanous_deviceDropped():
    print("DEVICE DROPPED!")

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