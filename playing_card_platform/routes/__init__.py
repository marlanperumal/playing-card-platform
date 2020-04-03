from flask_socketio import SocketIO, emit, send

socketio = SocketIO(cors_allowed_origins="http://localhost:3000")


@socketio.on("message")
def handle_message(message):
    send(f"Replying to: {message}")
    print("received message: " + message)


@socketio.on("connect")
def on_connect():
    emit("welcome", {"data": "test"})
