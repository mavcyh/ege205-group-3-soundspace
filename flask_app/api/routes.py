from flask_restx import Resource
from flask_app import ns
from flask_app import socketio
from flask_app.database.crud import create_booking, is_time_slot_available, get_volume_data
from flask import request, jsonify
from .models import volume_model
#region BOOKING

@ns.route("/bookings")
class create_bookings(Resource):
    def post(self):
        start_datetime = request.json.get("startTime")
        end_datetime = request.json.get("endTime")
        locker_ids = request.json.get("lockerIds", [])
        email = request.json.get("email")
        is_time_slot_available(start_datetime, end_datetime)

        if not is_time_slot_available(start_datetime, end_datetime):
            return jsonify({"message": "Booking slot is not available!"}), 409
        
        if not start_datetime or not end_datetime:
            return jsonify({"message": "Booking date, start time, and end time are required."}), 400
        
        create_booking(start_datetime, end_datetime, locker_ids, email)

@ns.route("/volume")
class show_volume(Resource):
    @ns.marshal_list_with(volume_model)
    def get(self):
        return get_volume_data()

#endregion BOOKING

#region TEST
    
@ns.route("/test/start-session")
class start_session(Resource):
    def post(self):
        TxData = {
                "session_duration_left": 30,
                "maximum_volume_level": 10
        }
        socketio.emit("serverToSessionInfo_connected", TxData)
        
@ns.route("/test/end-session")
class end_session(Resource):
    def post(self):
        TxData = {
                "session_duration_left": 0,
                "maximum_volume_level": 10
        }
        socketio.emit("serverToSessionInfo_connected", TxData)

@ns.route("/test/change-door-password")
class change_door_password(Resource):
    def post(self):
        TxData = {
            "master_password": "111111",
            "temporary_password": "123412"
        }
        socketio.emit("serverToRoomDoor_updatePasswords", TxData)


#endregion TEST