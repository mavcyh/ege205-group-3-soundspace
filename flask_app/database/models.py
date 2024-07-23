from flask_app import db, Numeric, REAL


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(255), unique=True, nullable=False)
#     password = db.Column(db.String(255), nullable=False)
#     email = db.Column(db.String(255))
    
#     def __repr__(self):
#         return f"User('{self.username}', '{self.email}')"
    

booking_instrument = db.Table('booking_instrument',
    db.Column('booking_start_datetime', db.String, db.ForeignKey('booking.start_datetime'), primary_key=True),
    db.Column('locker_id', db.Integer, db.ForeignKey('instrument.locker_id'), primary_key=True)
)

class Booking(db.Model):
    start_datetime = db.Column(db.String, primary_key=True, nullable=False)
    end_datetime = db.Column(db.String, nullable=False)
    locker_numbers = db.relationship('Instrument', secondary=booking_instrument,
        backref=db.backref('bookings'))
    email = db.Column(db.String, nullable=False)  
    device_dropped = db.Column(db.Boolean, default=False)     

# TODO method to dynamically change "wear" of instruments e.g. 60% after 100 hours of active use + 3 months passive deterioration
class Instrument(db.Model):
    locker_id = db.Column(db.Integer, primary_key=True, nullable=False)
    instrument_name = db.Column(db.String(255), nullable=False)
    name_abbr = db.Column(db.String(15), nullable=False)
    wear_value = db.Column(db.REAL, nullable=False)
    price = db.Column(Numeric(precision=10, scale=2), nullable=False)  

class Volume(db.Model):
    time_stamp = db.Column(db.String(15), primary_key=True, nullable=False)
    volume_limit = db.Column(db.Integer, nullable=False)
    volume_data = db.Column(db.Integer, nullable=False)
