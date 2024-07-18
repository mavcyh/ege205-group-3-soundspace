import eventlet
from eventlet import wsgi
from flask_app import app, db

# CREATE DATABASE ON FIRST RUN (in newly created "instance" folder)
with app.app_context():
    db.create_all()

wsgi.server(eventlet.listen(("192.168.88.9", 5000)), app)