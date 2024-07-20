from flask import request, jsonify
from flask_app import app, db
from flask_app.database.models import Booking, Instrument


def is_time_slot_available(date, start_time, end_time):
    existing_bookings = Booking.query.filter_by(booking_date=date).all()
    for booking in existing_bookings:
        if start_time < booking.end_time and end_time > booking.start_time:
            return False
    return True

def create_booking(booking_date, start_time, end_time, instrument_ids):
    
    id = f"{booking_date}T{start_time[:5]}"

    new_booking = Booking(id=id, booking_date=booking_date, start_time=start_time, end_time=end_time)
    for instrument_id in instrument_ids:
        instrument = Instrument.query.get(instrument_id)
        if instrument:
            new_booking.instruments.append(instrument)
            
        db.session.add(new_booking)
        db.session.commit()

    