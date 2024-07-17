from flask_app import db

# booking_instrument = db.Table('booking_instrument',
#     db.Column('booking_id', db.Integer, db.ForeignKey('booking.id'), primary_key=True),
#     db.Column('instrument_id', db.Integer, db.ForeignKey('instrument.id'), primary_key=True)
# )

#class User(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(255), unique=True, nullable=False)
    # password = db.Column(db.String(255), nullable=False)
    # email = db.Column(db.String(255))
    
    # def __repr__(self):
    #     return f"User('{self.username}', '{self.email}')"
    
# TODO user_id as foreign key, method to store date and time of booking
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_date = db.Column(db.String, nullable=False)
    start_time = db.Column(db.String, nullable=False)
    end_time = db.Column(db.String, nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "bookingDate": self.booking_date,
            "startTime": self.start_time,
            "endTime": self.end_time
        }
    
    #device_dropped = db.Column(db.Boolean, default=False)
    #instruments = db.relationship('Instrument', secondary=booking_instrument, lazy='subquery',
        #backref=db.backref('bookings', lazy=True))
    
#class Locker(db.Model):
    #locker_id = db.column(db.Integer, primary_key=True)
    #instrument_id = db.column(db.Integer, nullable=False)


# TODO method to dynamically change "wear" of instruments e.g. 60% after 100 hours of active use + 3 months passive deterioration
#class Instrument(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(255), nullable=False)
    #name_abbr = db.column(db.String(15), nullable=False)
    #locker_number = db.Column(db.String(10), nullable=False)