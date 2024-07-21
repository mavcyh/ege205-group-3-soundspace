from flask_app import nsApi, nsAdmin, fields

volume_model = nsAdmin.model("Volume", {
    "time_stamp": fields.String,
    "volume_limit": fields.Integer,
    "volume_data": fields.Integer
})

create_booking_model = nsApi.model("Create Booking", {
    "start_datetime": fields.String,
    "end_datetime": fields.String,
    "lockers": fields.List(fields.Integer),
    "email": fields.String
})

# model for create booking (start_time, end_time, email, locker no.)

# ns.payload()

# 2 diff models (input model, and model for booking stuff)