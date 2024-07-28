import eventlet
from eventlet import wsgi
from flask_app import app, db
from flask_app.database.crud import insert_instrument_data, coded_booking

# CREATE DATABASE ON FIRST RUN (in newly created "instance" folder)
with app.app_context():
    db.create_all() #db.drop_all() for the first time
    # insert_instrument_data() # remember to comment out this line of code after running the code for the first time
wsgi.server(eventlet.listen(("0.0.0.0", 5000)), app)