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

reset_locker_wear_model = nsAdmin.model("Reset Locker Wear", {
    "locker_id": fields.Integer,
})

change_master_password_model = nsAdmin.model("Change Master Password", {
    "current_master_password": fields.String,
    "new_master_password": fields.String
})

# model for create booking (start_time, end_time, email, locker no.)

# ns.payload()

# 2 diff models (input model, and model for booking stuff)