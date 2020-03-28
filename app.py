from playing_card_platform import create_app, db, methods, models

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "methods": methods, "models": models}
