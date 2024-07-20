from flask_restx import Resource
from flask_app import ns
from flask_app import socketio
from flask_app.database.crud import create_booking, is_time_slot_available
from flask import request, jsonify
#region BOOKING

@ns.route("/bookings")
class create_bookings(Resource):
    def post(self):
        booking_date = request.json.get("bookingDate")
        start_time = request.json.get("startTime")
        end_time = request.json.get("endTime")
        instrument_ids = request.json.get("instrumentIds", [])
        is_time_slot_available(booking_date, start_time, end_time)

        if not is_time_slot_available(booking_date, start_time, end_time):
            return jsonify({"message": "Booking date, start time, and end time are required."}), 409
        
        if not booking_date or not start_time or not end_time:
            return jsonify({"message": "Booking date, start time, and end time are required."}), 400
        
        create_booking(booking_date, start_time, end_time, instrument_ids)

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