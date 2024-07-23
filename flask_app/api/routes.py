from flask import jsonify
from flask_restx import Resource
from flask_app import nsApi, nsAdmin
from flask_app import socketio
from flask_app.database.crud import create_booking, is_time_slot_available, get_volume_data
from .models import volume_model, create_booking_model, reset_locker_wear_model, change_master_password_model


#region BOOKING PAGE

# Return an array of all the bookings with a start time beyond the current datetime.
# Function: Blocking out the timeslots on the website.
# AND return an array of all the instruments lockers.
# Function: Selection of the instrument (in reality, locker) to book on the website.
@nsApi.route("/booking-and-locker-info")
class api_booking_and_locker_info(Resource):
    def get(self):
        data = {'booking-info': None,
                'locker-info': None }
        return data

# Accept input to create a new booking
@nsApi.route("/create-booking")
class api_create_booking(Resource):
    @nsApi.expect(create_booking_model)
    def post(self):
        start_datetime = nsApi.payload["start_datetime"]
        end_datetime = nsApi.payload["end_datetime"]
        locker_ids = nsApi.payload["lockers"]
        email = nsApi.payload["email"]
        
        if not is_time_slot_available(start_datetime, end_datetime):
            return jsonify({"message": "Booking slot is not available!"}), 409
        
        if not start_datetime or not end_datetime:
            return jsonify({"message": "Booking date, start time, and end time are required."}), 400
        
        create_booking(start_datetime, end_datetime, locker_ids, email)

#endregion BOOKING PAGE


#region ADMIN PAGE

# Return an array of all the volume data
@nsAdmin.route("/current-session-volume-data")
class admin_current_session_volume_data(Resource):
    @nsApi.marshal_list_with(volume_model)
    def get(self):
        return get_volume_data()

@nsAdmin.route("/instrument-data")
class admin_instrument_data(Resource):
    def get(self):
        return None

@nsAdmin.route("/bookings")
class admin_bookings(Resource):
    def get(self):
        return None

@nsAdmin.route("/reset-locker-wear")
class admin_reset_locker_wear(Resource):
    @nsAdmin.expect(reset_locker_wear_model)
    def post(self):
        locker_id = nsApi.payload["locker_id"]
        print(locker_id)

@nsAdmin.route("change-master-password")
class admin_change_master_password(Resource):
    @nsAdmin.expect(change_master_password_model)
    def post(self):
        current_master_password = nsApi.payload["current_master_password"]
        new_master_password = nsApi.payload["new_master_password"]
        print(f"Current master password: {current_master_password}\nNew master password: {new_master_password}")


#endregion ADMIN PAGE


#region TEST

@nsApi.route("/test/start-session")
class route_start_session(Resource):
    def post(self):
        TxData = {
                "session_duration_left": 30,
                "maximum_volume_level": 10
        }
        socketio.emit("serverToSessionInfo_connected", TxData)
        
@nsApi.route("/test/end-session")
class route_end_session(Resource):
    def post(self):
        TxData = {
                "session_duration_left": 0,
                "maximum_volume_level": 10
        }
        socketio.emit("serverToSessionInfo_connected", TxData)

@nsApi.route("/test/change-door-password")
class route_change_door_password(Resource):
    def post(self):
        TxData = {
            "master_password": "111111",
            "temporary_password": "123412"
        }
        socketio.emit("serverToRoomDoor_updatePasswords", TxData)

#endregion TEST