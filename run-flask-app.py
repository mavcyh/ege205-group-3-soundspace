import eventlet
eventlet.monkey_patch(thread=True, time=True)
from eventlet import wsgi
from flask_app import app, db, socketio
from flask_app.core.core import core_per_minute
from flask_app.database.crud import insert_instrument_data

# To be used for debugging: clears the entire database, creates everything afresh, and inserts default instrument data
with app.app_context():
    db.drop_all() # Comment this out on very first running of code (instance/db.sqlite3 does not exist yet): db will not be available yet
    db.create_all()
    insert_instrument_data()
    core_per_minute()

socketio.run(app, host='0.0.0.0', port=5000)