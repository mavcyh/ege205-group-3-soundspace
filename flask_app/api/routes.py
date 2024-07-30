from flask import jsonify
from flask_restx import Resource
from flask_app import nsApi, nsAdmin
from flask_app import socketio
from flask_app.database.crud import *
from .models import *
from flask_app.database.crud import *
from .models import *
from flask_app.socketio_events.bbbw import change_master_password
from flask_app.core.mailer import send_confirmation_booking_email
from flask_app.core.mailer import send_confirmation_booking_email
import random
from datetime import datetime
import pytz


#region BOOKING PAGE

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
        locker_ids = nsApi.payload["locker_ids"]
        email = nsApi.payload["email"]
        if not is_time_slot_available(start_datetime, end_datetime):
            return {"error_message": "Timeslot is not available! Refresh the page."}, 400
        
        temporary_password = str(random.randint(0, 999999)).zfill(6)
        create_booking(start_datetime, end_datetime, locker_ids, email, temporary_password)
        
        def convert_to_formatted_singapore_datetime(iso_date_string):
            utc_datetime = datetime.fromisoformat(iso_date_string.replace('Z', '+00:00'))
            singapore_datetime = utc_datetime.astimezone(pytz.timezone('Asia/Singapore'))
            formatted_datetime = singapore_datetime.strftime('%d/%m/%Y %H:%M')
            return formatted_datetime
        
        start_datetime = convert_to_formatted_singapore_datetime(start_datetime)
        end_datetime = convert_to_formatted_singapore_datetime(end_datetime)
        try:
            send_confirmation_booking_email(temporary_password, start_datetime, end_datetime, get_instrument_names_from_locker(locker_ids), email)
        except Exception as error:
            print("Failed to send email.")
            print(error)
            return {"error_message": "Something went wrong when trying to send you the email. Please try again later."}, 400
            
        
#endregion BOOKING PAGE


#region ADMIN PAGE

@nsAdmin.route("/humidity-data")
class admin_humidity_data(Resource):
    @nsApi.marshal_list_with(humidity_model)
    def get(self):
        return get_humidity_data()

@nsAdmin.route("/session-volume-data")
class admin_session_volume_data(Resource):
    @nsApi.expect(get_booking_start_datetime)
    @nsApi.marshal_list_with(volume_model)
    def post(self):
        booking_start_datetime = nsApi.payload["start_datetime"]       
        return get_volume_data_by_start_datetime(booking_start_datetime)

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

@nsAdmin.route("/change-master-password")
class admin_change_master_password(Resource):
    @nsAdmin.expect(change_master_password_model)
    def post(self):
        new_master_password = nsApi.payload["new_master_password"]
        print(f"New master password: {new_master_password}")
        TxData = {
            "new_master_password": new_master_password
        }
        socketio.emit("serverToRoomDoor_updateMasterPassword", TxData)


#endregion ADMIN PAGE