from flask_app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

# TODO user_id as foreign key, method to store date and time of booking
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)

# TODO method to dynamically change "wear" of instruments e.g. 60% after 100 hours of active use + 3 months passive deterioration
class Instrument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    # Max length that can be shown on the BBBW OLED is 15 chars
    name_abbr = db.Column(db.String(15), nullable=False)