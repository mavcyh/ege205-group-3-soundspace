from flask_restx import Resource
from flask_app import ns
from flask_app import socketio

#region TEST
    
@ns.route("/test/start-session")
class start_session(Resource):
    def post(self):
        TxData = {
                "session_duration_left": 30,
                "maximum_volume_level": 10
        }
        socketio.emit("serverToSessionInfo_connected", TxData)
        
@ns.route("/test/end-session")
class end_session(Resource):
    def post(self):
        TxData = {
                "session_duration_left": 0,
                "maximum_volume_level": 10
        }
        socketio.emit("serverToSessionInfo_connected", TxData)

@ns.route("/test/change-door-password")
class change_door_password(Resource):
    def post(self):
        TxData = {
            "master_password": "111111",
            "temporary_password": "123412"
        }
        socketio.emit("serverToRoomDoor_updatePasswords", TxData)


#endregion TEST