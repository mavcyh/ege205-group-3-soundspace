from flask_app import ns, fields

volume_model = ns.model("Volume", {
    "time_stamp": fields.String,
    "volume_limit": fields.Integer,
    "volume_data": fields.Integer
})

# model for create booking (start_time, end_time, email, locker no.)

# ns.payload()

# 2 diff models (input model, and model for booking stuff)