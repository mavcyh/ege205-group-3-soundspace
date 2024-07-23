from flask_app import nsApi, nsAdmin, fields

volume_model = nsAdmin.model("Volume", {
    "time_stamp": fields.String,
    "volume_limit": fields.Integer,
    "volume_data": fields.Integer
})

create_booking_model = nsApi.model("Create Booking", {
    "start_datetime": fields.String,
    "end_datetime": fields.String,
    "lockers": fields.List(fields.String),
    "email": fields.String
})

reset_locker_wear_model = nsAdmin.model("Get Locker Wear", {
    "locker_id": fields.String
})

send_locker_wear_model = nsAdmin.model("Send Locker Wear", {
    "wear_value": fields.List(fields.String)
})

change_master_password_model = nsAdmin.model("Change Master Password", {
    "current_master_password": fields.String,
    "new_master_password": fields.String
})

# Wear value increases from 0 to 100 (Can exceed 100)
# Create a model to update api with wear value (Sends an integer, if resetted send 0 to api)

# model for create booking (start_time, end_time, email, locker no.)

# ns.payload()

# 2 diff models (create_booking_model and display_booking_model)