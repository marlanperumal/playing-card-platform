from flask_socketio import SocketIO

socketio = SocketIO()


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
