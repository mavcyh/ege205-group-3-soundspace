from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Numeric, REAL
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_restx import Api, Namespace, fields

app = Flask(__name__)
socketio = SocketIO(app, async_mode="eventlet")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)
ns = Namespace("api")
api = Api(app)
api.add_namespace(ns)

from flask_app.core import core, mailer
from flask_app.socketio_events import bbbw, nextjs
from flask_app.database import models, crud
from flask_app.api import routes, models