from flask import request, jsonify, json
from flask_app import app, db
from flask_app.database.models import Booking, Instrument, Volume, booking_instrument
from datetime import datetime

def convert_to_datetime(datetime_str):
    return datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')

def is_time_slot_available(start_datetime, end_datetime):
    start_datetime_obj = convert_to_datetime(start_datetime)
    end_datetime_obj = convert_to_datetime(end_datetime)

    overlapping_bookings = Booking.query.filter(
        (Booking.start_datetime < end_datetime_obj.isoformat()) &
        (Booking.end_datetime > start_datetime_obj.isoformat())
    ).all()

    for booking in overlapping_bookings:
        if convert_to_datetime(booking.start_datetime) < end_datetime_obj and convert_to_datetime(booking.end_datetime) > start_datetime_obj:
            return False

    return True
        
def create_booking(start_datetime, end_datetime, locker_ids, email):
    new_booking = Booking(start_datetime=start_datetime, end_datetime=end_datetime, locker_id=locker_ids, email=email)
    for locker_id in locker_ids:
        locker = Instrument.query.get(locker_id)
        if locker:
            new_booking.locker_numbers.append(locker)
    print(new_booking)
    db.session.add(new_booking)
    db.session.commit()

def write_volume_level_data(time_stamp, volume_data, volume_limit):
    volume_data_json = json.dumps(volume_data).strip('[]')

    new_volume = Volume(time_stamp=time_stamp, volume_data=volume_data_json, volume_limit=volume_limit)
    db.session.add(new_volume)
    db.session.commit()

def get_current_session_volume_data():
    start_datetime, end_datetime = get_session_active()
    if start_datetime and end_datetime:
        start_datetime_obj = convert_to_datetime(start_datetime)
        end_datetime_obj = convert_to_datetime(end_datetime)
        
        current_session_volumes = Volume.query.filter(
            (Volume.time_stamp >= start_datetime_obj.isoformat()) &
            (Volume.time_stamp <= end_datetime_obj.isoformat())
        ).all()
        
        return current_session_volumes
    else:
        return "No active session"
    
def equipment_dropped():
    start_datetime, end_datetime = get_session_active()
    
    if start_datetime and end_datetime:
        ongoing_booking = Booking.query.filter(
            Booking.start_datetime == start_datetime,
            Booking.end_datetime == end_datetime
        ).first()
        
        if ongoing_booking:
            # Update the device_dropped field to True(1)
            ongoing_booking.device_dropped = True
            db.session.commit()

def get_session_active():
    now = datetime.now()
    ongoing_bookings = Booking.query.filter(
        (Booking.start_datetime <= now.isoformat()) &
        (Booking.end_datetime >= now.isoformat())
    ).all()

    if ongoing_bookings:
        session = ongoing_bookings[0]  
        print(session.start_datetime, "  " ,session.end_datetime)
        return session.start_datetime, session.end_datetime
    else:
        print("No session ongoing")
        return None, None

def get_booking_availability_and_instruments():
    now = datetime.now().strftime('%Y-%m-%dT%H:%M')
    future_bookings = Booking.query.filter(Booking.start_datetime > now).all()
    result = []
    for booking in future_bookings:
        locker_ids = [instrument.locker_id for instrument in booking.locker_numbers]
        booking_dict = {
            'start_time': booking.start_datetime,
            'end_time': booking.end_datetime,
            'email': booking.email,
            'locker_ids': locker_ids
        }
        result.append(booking_dict)
    return(result)

def insert_instrument_data():
    data = [
        ("1", "Fender Stratocaster", "F Strat", 21.90, 2.50),
        ("2", "SR300E", "Ib SR300E", 11.90, 1.50)
    ]
    
    for locker_id, instrument_name, name_abbr, wear_value, price in data:
        new_instrument = Instrument(
            locker_id=locker_id,
            instrument_name=instrument_name,
            name_abbr=name_abbr,
            wear_value=wear_value,
            price=price
        )
        db.session.add(new_instrument)
    db.session.commit()


def reset_wear_value(locker_id):
    instrument = Instrument.query.filter_by(locker_id=locker_id).first()
    if instrument:
        instrument.wear_value = 0
        db.session.commit()

def get_wear_values():
    instrument_1 = Instrument.query.filter_by(locker_id="1").first()
    instrument_2 = Instrument.query.filter_by(locker_id="2").first()

    # Return the wear values or a default value if not found
    wear_value_1 = f"{instrument_1.wear_value:.2f}" if instrument_1 else "Not Found"
    wear_value_2 = f"{instrument_2.wear_value:.2f}" if instrument_2 else "Not Found"

    # Return as a list of values
    return [wear_value_1, wear_value_2]

def update_instrument_wear_values():
    start_datetime, end_datetime = get_session_active()
    
    if start_datetime and end_datetime:
        # Get the list of booked instruments for the ongoing session
        booked_instruments = db.session.query(booking_instrument).filter_by(booking_start_datetime=start_datetime).all()
        booked_instrument_ids = [instrument.locker_id for instrument in booked_instruments]

        # Update the wear value for each booked instrument
        for locker_id in booked_instrument_ids:
            instrument = Instrument.query.filter_by(locker_id=locker_id).first()
            if instrument:
                instrument.wear_value += 0.5  # Increase wear value by 0.5 for in-use instruments
                db.session.commit()

    else:
        # If no active session, update wear value for all instruments
        all_instruments = Instrument.query.all()
        for instrument in all_instruments:
            instrument.wear_value += 0.1  # Increase wear value by 0.1 for non-active instruments
            db.session.commit()

# function to update wear values

# function to reset? from current value to 0, may be combined with update wear values function


# locker(price etc.)

# Things to do: update_events function get humidity value, use get_session_active for ir motion and possibly send to admin page?

# Add necessary api models for displaying booking details