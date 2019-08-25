from flask_cors import CORS
from flask_socketio import SocketIO

cors = CORS(supports_credentials=True)
io = SocketIO()
global current_user
current_user = None
