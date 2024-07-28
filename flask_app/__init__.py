from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Numeric
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_restx import Api, Namespace, fields

app = Flask(__name__)
socketio = SocketIO(app, async_mode="eventlet")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)
nsApi = Namespace("api")
nsAdmin = Namespace("admin")
api = Api(app)
api.add_namespace(nsApi)
api.add_namespace(nsAdmin)

from flask_app.core import core, mailer
from flask_app.socketio_events import bbbw, nextjs
from flask_app.database import models, crud
from flask_app.api import models, routes