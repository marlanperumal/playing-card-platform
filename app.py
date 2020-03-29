from playing_card_platform import create_app, db, methods, models
from playing_card_platform.routes import socketio
from config import Config

app = create_app(Config)


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "methods": methods, "models": models}


if __name__ == "__main__":
    socketio.run(app)
