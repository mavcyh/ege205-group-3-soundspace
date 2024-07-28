from flask import jsonify
from flask_restx import Resource
from flask_app import nsApi, nsAdmin
from flask_app import socketio
from flask_app.database.crud import create_booking, is_time_slot_available, get_volume_data_by_start_datetime, reset_wear_value, get_wear_values, get_booking_availability_and_instruments, get_start_datetime, get_instrument_names_from_locker
from .models import volume_model, create_booking_model, reset_locker_wear_model, send_locker_wear_model, change_master_password_model, booking_availability_model, get_booking_start_datetime, master_password_model
from flask_app.socketio_events.bbbw import change_master_password
#region BOOKING PAGE

# Return an array of all the bookings with a start time beyond the current datetime.
# Function: Blocking out the timeslots on the website.
# AND return an array of all the instruments lockers.
# Function: Selection of the instrument (in reality, locker) to book on the website.
@nsApi.route("/booking-and-locker-info")
class api_booking_and_locker_info(Resource):
    @nsApi.marshal_list_with(booking_availability_model)
    def get(self):
        return get_booking_availability_and_instruments()

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
            return {"message": "Timeslot is not available!"}, 400
        
        create_booking(start_datetime, end_datetime, locker_ids, email)
#endregion BOOKING PAGE


#region ADMIN PAGE

# Return an array of all the volume data
@nsAdmin.route("/current-session-volume-data")
class admin_current_session_volume_data(Resource):
    @nsApi.expect(get_booking_start_datetime)
    @nsApi.marshal_with(volume_model)
    def post(self):
        booking_start_datetime = nsApi.payload["start_datetime"]
        if booking_start_datetime == "no start_datetime":
            return get_volume_data_by_start_datetime(booking_start_datetime)
        
        get_volume = get_volume_data_by_start_datetime(booking_start_datetime)
        return get_volume

@nsAdmin.route("/change-master-password")
class update_master_password(Resource):
    @nsApi.expect(master_password_model)
    def post(self):
        master_password = nsApi.payload["master_password"]
        change_master_password(master_password)

@nsAdmin.route("/all-bookings")
class all_bookings(Resource):
    @nsApi.marshal_list_with(get_booking_start_datetime)
    def get(self):
        all_start_datetime = get_start_datetime()
        return {"start_datetime": all_start_datetime}

@nsAdmin.route("/instrument-data")
class admin_instrument_data(Resource):
    def get(self):
        return None

@nsAdmin.route("/bookings")
class admin_bookings(Resource):
    def get(self):
        return None

@nsAdmin.route("/get-locker-wear")
class admin_get_locker_wear(Resource):
    @nsAdmin.marshal_list_with(send_locker_wear_model)
    def get(self):
        wear_values = get_wear_values()
        return {"wear_value": wear_values}

@nsAdmin.route("/reset-locker-wear")
class admin_reset_locker_wear(Resource):
    @nsAdmin.expect(reset_locker_wear_model)
    def post(self):
        locker_id = nsApi.payload["locker_id"]
        reset_wear_value(locker_id)

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