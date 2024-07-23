from flask import request, jsonify, json
from flask_app import app, db
from flask_app.database.models import Booking, Instrument, Volume
from datetime import datetime

def is_time_slot_available(start_datetime, end_datetime):
    # Convert datetime strings to datetime objects for comparison
    start_datetime_obj = datetime.strptime(start_datetime, '%Y-%m-%dT%H:%M')
    end_datetime_obj = datetime.strptime(end_datetime, '%Y-%m-%dT%H:%M')

    # Query for existing bookings within the given time range
    existing_bookings = Booking.query.filter(
        (Booking.start_datetime <= start_datetime_obj) & 
        (Booking.end_datetime >= end_datetime_obj)
    ).all()

    # Check if there are any overlapping bookings
    for booking in existing_bookings:
        if start_datetime_obj < booking.end_datetime and end_datetime_obj > booking.start_datetime:
            return False

    return True

def create_booking(start_datetime, end_datetime, locker_ids, email):
    new_booking = Booking(start_datetime=start_datetime, end_datetime=end_datetime, email=email)
    for locker_id in locker_ids:
        locker = Instrument.query.get(locker_id)
        if locker:
            new_booking.instruments.append(locker)
    print(new_booking)
    db.session.add(new_booking)
    db.session.commit()

def write_volume_level_data(time_stamp, volume_data, volume_limit):
    volume_data_json = json.dumps(volume_data).strip('[]')

    new_volume = Volume(time_stamp=time_stamp, volume_data=volume_data_json, volume_limit=volume_limit)
    db.session.add(new_volume)
    db.session.commit()

def get_volume_data():
    # TODO CHECK IF THERE IS AN ACTIVE SESSION, IF SO, FIND THE START TIME AND END TIME
    # THEN, CHECK IF THE VOLUME DATA'S TIMESTAMP IS WITHIN THE START TIME AND END TIME.
    volumes = Volume.query.all()
    return volumes

def print_volume_data():
    volume_data_list = get_volume_data()
    for volume_data in volume_data_list:
        print(volume_data)

def get_booking_availability_and_instruments():
    now = datetime.now().strftime('%Y-%m-%dT%H:%M')
    future_bookings = Booking.query.filter(Booking.start_datetime > now).all()
    result = []
    for booking in future_bookings:
        locker_ids = [instrument.locker_id for instrument in booking.instruments]
        booking_dict = {
            'start_time': booking.start_datetime,
            'end_time': booking.end_datetime,
            'email': booking.email,
            'locker_ids': locker_ids
        }
        result.append(booking_dict)
    return result
# return each locker(name, price)