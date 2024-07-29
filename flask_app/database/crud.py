from flask import json
from flask_app import app, db
from flask_app.database.models import Booking, Instrument, Volume, Events, Humidity, booking_instrument
from datetime import datetime, timezone, timedelta
from decimal import Decimal
import random

# Database format TO TZ format
def convert_to_utc_datetime(datetime_str):
    # Parse the datetime string to a naive datetime object
    naive_dt = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M")
    
    # Convert to a timezone-aware datetime in UTC
    utc_dt = naive_dt.replace(tzinfo=timezone.utc)
    
    return utc_dt

# TZ format TO Python format
def create_datetime_with_tz(datetime_str):
    # Directly convert string to timezone-aware datetime
    return datetime.fromisoformat(datetime_str.replace("Z", "+00:00"))

# TZ format TO Database format
def format_datetime(iso_datetime_str):
    # Parse the ISO 8601 string to a datetime object
    dt = datetime.fromisoformat(iso_datetime_str.replace("Z", "+00:00"))
    
    # Format the datetime object to 'YYYY-MM-DDTHH:MM' as a string
    formatted_str = dt.strftime('%Y-%m-%dT%H:%M')
    
    return formatted_str

def format_time(datetime_str):
    datetime_obj = datetime.fromisoformat(datetime_str).replace(tzinfo=timezone.utc)
    return datetime_obj.strftime('%H:%M')

def is_time_slot_available(start_datetime, end_datetime):
    start_datetime_obj = create_datetime_with_tz(start_datetime)
    end_datetime_obj = create_datetime_with_tz(end_datetime)

    overlapping_bookings = Booking.query.filter(
        (Booking.start_datetime < end_datetime_obj.isoformat()) &
        (Booking.end_datetime > start_datetime_obj.isoformat())
    ).all()

    for booking in overlapping_bookings:
        booking_start = convert_to_utc_datetime(booking.start_datetime)
        booking_end = convert_to_utc_datetime(booking.end_datetime)
        if booking_start < end_datetime_obj and booking_end > start_datetime_obj:
            return False

    return True

def create_booking(start_datetime, end_datetime, locker_ids, email, temporary_password):
    formatted_start_datetime = format_datetime(start_datetime)
    formatted_end_datetime = format_datetime(end_datetime)
    new_booking = Booking(start_datetime=formatted_start_datetime, end_datetime=formatted_end_datetime, email=email, temporary_password=temporary_password)
    for locker_id in locker_ids:
        locker = Instrument.query.get(locker_id)
        if locker:
            new_booking.locker_numbers.append(locker)
    db.session.add(new_booking)
    db.session.commit()
    print("New booking created.")

def write_volume_level_data(time_stamp, volume_data, volume_limit):
    volume_data_json = json.dumps(volume_data).strip('[]')
    start_datetime, end_datetime = get_session_active()

    if start_datetime and end_datetime:
        new_volume = Volume(time_stamp=time_stamp, volume_data=volume_data_json, volume_limit=volume_limit)
        db.session.add(new_volume)  

    db.session.commit()

def delete_specific_booking():
    # Hardcoded start_datetime string
    start_datetime_str = "2024-07-27T09:00"
    
    # Query the booking to delete
    booking_to_delete = Booking.query.filter_by(start_datetime=start_datetime_str).first()
    
    if booking_to_delete:
        db.session.delete(booking_to_delete)
        db.session.commit()
        print("Booking deleted successfully.")
    else:
        print("No booking found with the specified start_datetime.")

def get_current_session_volume_data():
    start_datetime, end_datetime = get_session_active()
    if start_datetime and end_datetime:
        start_datetime_obj = format_datetime(start_datetime)
        end_datetime_obj = format_datetime(end_datetime)
        
        current_session_volumes = Volume.query.filter(
            (Volume.time_stamp >= start_datetime_obj) &
            (Volume.time_stamp <= end_datetime_obj)
        ).all()
        
        # Adjust each volume's time_stamp to display only the time
        adjusted_volumes = []
        for volume in current_session_volumes:
            volume_dict = {
                'id': volume.id,
                'time_stamp': format_time(volume.time_stamp),
                'volume_limit': volume.volume_limit,
                'volume_data': volume.volume_data
            }
            adjusted_volumes.append(volume_dict)
        
        return adjusted_volumes
    else:
        return "No active session"

def get_volume_data_by_start_datetime(start_datetime):

    if start_datetime == "":
        start_datetime_obj, end_datetime_obj = get_session_active()
        if not start_datetime_obj or not end_datetime_obj:
            volume_data_list = []
            volume_dict = {
                'time_stamp': "0",
                'volume_limit': "0",
                'volume_data': "0"
            }
            volume_data_list.append(volume_dict)
            return volume_data_list

    else:
        start_datetime_obj = format_datetime(start_datetime)
        booking = Booking.query.filter_by(start_datetime=start_datetime_obj).first()
        end_datetime_obj = format_datetime(booking.end_datetime)

    # Filter volumes that fall within the booking period
    volumes = Volume.query.filter(
        (Volume.time_stamp >=  start_datetime_obj) &
        (Volume.time_stamp <= end_datetime_obj)
    ).all()
    
    
    volume_data_list = []
    for volume in volumes:
        volume_dict = {
            'time_stamp': format_time(volume.time_stamp),
            'volume_limit': volume.volume_limit,
            'volume_data': volume.volume_data
        }
        volume_data_list.append(volume_dict)
    
    return volume_data_list

def get_instrument_names_from_locker(locker_ids):
    if not locker_ids:
        return []
    
    instrument_names = []
    for locker_id in locker_ids:
        instrument = Instrument.query.filter_by(locker_id=locker_id).first()
        if instrument:
            instrument_names.append(instrument.instrument_name)

    return instrument_names

def get_session_active():
    now = datetime.now(timezone.utc).isoformat()
    ongoing_bookings = Booking.query.filter(
        (Booking.start_datetime <= now) &
        (Booking.end_datetime >= now)
    ).all()

    if ongoing_bookings:
        session = ongoing_bookings[0]  
        return session.start_datetime, session.end_datetime
    else:
        return None, None

def get_session_active_core():
    now = datetime.now(timezone.utc).isoformat()
    ongoing_bookings = Booking.query.filter(
        (Booking.start_datetime <= now) &
        (Booking.end_datetime >= now)
    ).all()

    if ongoing_bookings:
        session = ongoing_bookings[0]  
        return convert_to_utc_datetime(session.start_datetime), convert_to_utc_datetime(session.end_datetime)
    else:
        return None, None

def get_start_datetime():
    all_bookings = Booking.query.all()

    # Extract start_datetime from each booking
    start_datetimes = [booking.start_datetime for booking in all_bookings]
    
    print (start_datetimes)
    return start_datetimes


def get_booking_availability_and_instruments():
    now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M') 

    current_bookings = Booking.query.filter(Booking.start_datetime > now).all()
    current_bookings_list = []
    for booking in current_bookings:
        booking_dict = {
            'start_datetime': convert_to_utc_datetime(booking.start_datetime),
            'end_datetime': convert_to_utc_datetime(booking.end_datetime)
        }
        current_bookings_list.append(booking_dict)
    
    instruments = Instrument.query.all()
    instrument_data = []
    for instrument in instruments:
        instrument_dict = {
            "locker_id": instrument.locker_id,
            "instrument_name": instrument.instrument_name,  
            "price_per_hour": float(instrument.price)  
        }
        instrument_data.append(instrument_dict)

    results = {
        "current_bookings": current_bookings_list,
        "instrument_data": instrument_data
    }

    return results

def insert_instrument_data():
    data = [
        ("1", "Fender Stratocaster", 21.90, 2.50),
        ("2", "Ibanez SR300E", 11.90, 1.50)
    ]
    
    for locker_id, instrument_name, wear_value, price in data:
        new_instrument = Instrument(
            locker_id=locker_id,
            instrument_name=instrument_name,
            wear_value=wear_value,
            price=price
        )
        db.session.add(new_instrument)
    db.session.commit()


def insert_humidity_data(humidity_value):
    current_time_utc = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M') 
    time_stamp = format_time(current_time_utc)
    new_humidity = Humidity(time_stamp=time_stamp, humidity=humidity_value)
    db.session.add(new_humidity)
    db.session.commit()

def get_humidity_data():    
    # Get the current UTC time and calculate the time two hours ago
    now = datetime.now(timezone.utc)
    two_hours_ago = now - timedelta(hours=2)

    # Fetch all humidity data from the database
    all_data = Humidity.query.all()

    filtered_data = []

    for record in all_data:
        # Extract the record's time_stamp
        record_time_str = record.time_stamp

        # Convert record's time_stamp to a datetime object for comparison
        # Assuming the record's date is today's date
        record_time = datetime.combine(now.date(), datetime.strptime(record_time_str, '%H:%M').time(), tzinfo=timezone.utc)

        # Compare the record's datetime with the time two hours ago
        if record_time >= two_hours_ago:
            filtered_data.append({
                'time_stamp': record.time_stamp,
                'humidity_data': record.humidity
            })
    return filtered_data


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
                instrument.wear_value += Decimal(0.5)  # Increase wear value by 0.5 for in-use instruments
                db.session.commit()

    else:
        # If no active session, update wear value for all instruments
        all_instruments = Instrument.query.all()
        for instrument in all_instruments:
            instrument.wear_value += Decimal('0.1')   # Increase wear value by 0.1 for non-active instruments
            db.session.commit()

def update_event(event):
    datetime_str = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M')
    start_datetime, end_datetime = get_session_active()
    if event == "motion":
        if start_datetime is None and end_datetime is None:
            update_motion = Events(timestamp=datetime_str, event_names="Motion Detected!", severity=1)
            db.session.add(update_motion)
            db.session.commit()
    if event == "dropped":
        if start_datetime and end_datetime:
            update_dropped = Events(timestamp=datetime_str, event_names="Device Dropped!", severity=2)    
            db.session.add(update_dropped)
            ongoing_booking = Booking.query.filter(
                Booking.start_datetime == start_datetime,
                Booking.end_datetime == end_datetime
            ).first()

            if ongoing_booking:
                # Update the device_dropped field to True(1)
                ongoing_booking.device_dropped = True
                db.session.commit()
    if event == "door broken into":
        if start_datetime is None and end_datetime is None:
            update_door_broken_into = Events(timestamp=datetime_str, event_names="Door Broken into!", severity=3)
            db.session.add(update_door_broken_into)
            db.session.commit

def get_event():
    events = Events.query.all()
    event_list = []

    for event in events:
        event_dict = {
            'timestamp': event.timestamp,
            'event_name': event.event_names,
            'severity': event.severity
        }
        event_list.append(event_dict)

    return event_list

def coded_booking():
    # Define hardcoded parameters
    start_datetime = "2024-07-28T15:00:00.000Z"
    end_datetime = "2024-07-28T18:28:00.000Z"
    locker_ids = ["1", "2"]  # Example locker IDs
    email = "example@example.com"
    temporary_password = str(random.randint(0, 999999)).zfill(6)
    
    # Use the create_booking function to insert the booking
    create_booking(start_datetime, end_datetime, locker_ids, email, temporary_password)

