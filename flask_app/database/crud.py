from flask import request, jsonify
from flask_app import app, db
from flask_app.database.models import Booking


def is_time_slot_available(date, start_time, end_time):
    existing_bookings = Booking.query.filter_by(booking_date=date).all()
    for booking in existing_bookings:
        if start_time < booking.end_time and end_time > booking.start_time:
            return False
    return True

@app.route("/bookings", methods = ["POST"])
def create_booking():
    booking_date = request.json.get("bookingDate")
    start_time = request.json.get("startTime")
    end_time = request.json.get("endTime")
    if not is_time_slot_available(booking_date, start_time, end_time):
        return jsonify({'message': 'Time slot is already booked'}), 409
    
    print (booking_date, start_time, end_time)
    if not booking_date or not start_time or not end_time:
        return(
        jsonify({"message:": "You must include a booking date start time and end time!"}),
        400,
    )

    new_booking = Booking(booking_date=booking_date, start_time=start_time, end_time=end_time)
    try:
        db.session.add(new_booking)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    return jsonify({"message": "Booking created!"}), 201

