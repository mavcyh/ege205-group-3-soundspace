from flask import request, jsonify
from flask_app import app, db
from flask_app.database.models import Booking
from flask_app.database.models import Instrument

def is_time_slot_available(date, start_time, end_time):
    existing_bookings = Booking.query.filter_by(booking_date=date).all()
    for booking in existing_bookings:
        if start_time < booking.end_time and end_time > booking.start_time:
            return False
    return True

# def delete_row_by_id():
#     row_to_delete = Booking.query.filter_by(booking_date="2024-07-23").first()
#     if row_to_delete:
#         db.session.delete(row_to_delete)
#         db.session.commit()
#         return True  # Deletion successful
#     return False  # Row with specified ID not found

# with app.app_context():
#     delete_row_by_id()

@app.route("/bookings", methods = ["POST"])
def create_booking():
    booking_date = request.json.get("bookingDate")
    start_time = request.json.get("startTime")
    end_time = request.json.get("endTime")
    instrument_ids = request.json.get("instrumentIds", []) 

    if not is_time_slot_available(booking_date, start_time, end_time):
        return jsonify({'message': 'Time slot is already booked'}), 409
    
    id = f"{booking_date}T{start_time[:5]}"

    print (booking_date, start_time, end_time)
    if not booking_date or not start_time or not end_time:
        return(
        jsonify({"message:": "You must include a booking date start time and end time!"}),
        400,
    )

    new_booking = Booking(id=id, booking_date=booking_date, start_time=start_time, end_time=end_time)
    for instrument_id in instrument_ids:
        instrument = Instrument.query.get(instrument_id)
        if instrument:
            new_booking.instruments.append(instrument)

    try:
        db.session.add(new_booking)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    return jsonify({"message": "Booking created!"}), 201

@app.route("/instruments", methods=["POST"])
def add_instruments():
    instrument_name = request.json.get("instrumentName")
    name_abbr = request.json.get("nameAbbr")
    print(f"{instrument_name}, {name_abbr}")
    add_instrument = Instrument(instrument_name=instrument_name, name_abbr=name_abbr)
    db.session.add(add_instrument)
    db.session.commit()

# @app.route("/getInstruments", methods = ["GET"])
# def get_instruments():
#     instruments = Instrument.query.all()
#     instruments_data = [instrument.to_json() for instrument in instruments]
#     return jsonify({"instruments": instruments_data})