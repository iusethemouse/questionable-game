from app import app, db
from app.models import Room, User

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Room': Room, 'User': User}