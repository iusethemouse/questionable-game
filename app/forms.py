from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

from app.models import Room, User


class CreateRoomForm(FlaskForm):
    room_name = StringField('Create a room', validators=[DataRequired()])
    submit = SubmitField('Create')


class JoinRoomForm(FlaskForm):
    room_code = StringField('Join a room', validators=[DataRequired()])
    submit = SubmitField('Join')

    def validate_room_code(self, room_code):
        room = Room.query.filter_by(code=room_code.data).first()
        if room is None:
            raise ValidationError("Couldn't find the room you're looking for!")


class NewUserForm(FlaskForm):
    name = StringField('Enter your name', validators=[DataRequired()])
    submit = SubmitField('Save')

    def validate_name(self, name):
        user = User.query.filter_by(name=name.data).first()
        if user is not None:
            raise ValidationError("Name already taken, please choose a different one.")