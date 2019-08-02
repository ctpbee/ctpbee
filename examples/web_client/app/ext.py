from flask_socketio import SocketIO

io = SocketIO()
global current_user
current_user = None
