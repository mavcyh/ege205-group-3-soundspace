from flask_app import db, Numeric

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
    temporary_password = db.Column(db.String(6), nullable=False)  
    device_dropped = db.Column(db.Boolean, default=False)  

class Instrument(db.Model): # Change this class to Locker
    locker_id = db.Column(db.String, primary_key=True, nullable=False)
    instrument_name = db.Column(db.String(15), nullable=False)
    wear_value = db.Column(Numeric(precision=10, scale=2), nullable=False)
    price = db.Column(Numeric(precision=10, scale=2), nullable=False)

class Volume(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    time_stamp = db.Column(db.String(15), nullable=False)
    volume_limit = db.Column(db.Integer, nullable=False)
    volume_data = db.Column(db.Integer, nullable=False)

class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    timestamp = db.Column(db.String, nullable=False)
    event_names = db.Column(db.String, nullable=False)
    severity = db.Column(db.Integer, nullable=False)
    

class Humidity(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    time_stamp = db.Column(db.String, nullable=False)
    humidity = db.Column(db.Integer, nullable=False)

# Create a new table for the different events (Make use of get_session_active to check for the events)
# table events (Columns: id as primary key(Auto increment), timestamp where it happended, name of events, severity of offence)
# table events contains (Current datetime (id), item dropped, someone in room when session is not active
# someone tries to break into the locker, which locker? - check all events from bbbw)   
