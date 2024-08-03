from flask_app import nsApi, nsAdmin, fields

humidity_model = nsApi.model("Humidity", {
    "time_stamp": fields.String,
    "humidity_data": fields.Integer
})

volume_model = nsApi.model("Volume", {
    "time_stamp": fields.String,
    "volume_limit": fields.Integer,
    "volume_data": fields.Integer
})

humidity_model = nsApi.model("Humidity", {
    "time_stamp": fields.String,
    "humidity_data": fields.Integer
})

get_booking_start_datetime = nsApi.model("Get Start Datetime", {
    "start_datetime" : fields.String
})

create_booking_model = nsApi.model("Create Booking", {
    "start_datetime": fields.String,
    "end_datetime": fields.String,
    "locker_ids": fields.List(fields.String),
    "email": fields.String
})

reset_locker_wear_model = nsAdmin.model("Get Locker Wear", {
    "locker_id": fields.String
})

send_locker_wear_model = nsAdmin.model("Send Locker Wear", {
    "wear_value": fields.List(fields.String)
})

change_master_password_model = nsAdmin.model("Change Master Password", {
    "new_master_password": fields.String
})

master_password_model = nsAdmin.model("Update master password", {
    "master_password": fields.String                                      
})

events_model = nsApi.model("get all events", {
    "timestamp": fields.String,
    "event_name": fields.String,
    "severity": fields.Integer
})

instrument_roomData_model = nsApi.model("InstrumentData", {
    "locker_id": fields.String,
    "instrument_name": fields.String,
    "wear_value": fields.Float,
    "price_per_hour": fields.Float,
    "usage": fields.Boolean
})

room_data_model = nsApi.model("RoomData", {
    "room_door_status": fields.String,
    "instrument_data": fields.List(fields.Nested(instrument_roomData_model)),
    "loitering_detected": fields.Boolean,
    "item_dropped": fields.Boolean
})

instrument_data_model = nsApi.model("InstrumentData", {
    "locker_id": fields.String,
    "instrument_name": fields.String,
    "price_per_hour": fields.Float,
    "usage": fields.Boolean
})


current_booking_model = nsApi.model("CurrentBooking", {
    "start_datetime": fields.String,
    "end_datetime": fields.String
})


booking_availability_model = nsApi.model("BookingAvailability", {
    "current_bookings": fields.List(fields.Nested(current_booking_model)),
    "instrument_data": fields.List(fields.Nested(instrument_data_model))
})