from flask import render_template, redirect, flash, url_for, jsonify, request
from flask_login import current_user, login_user#, logout_user, login_required

from app import app, db
from app.forms import CreateRoomForm, JoinRoomForm, NewUserForm
from app.models import Room, User


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    create_form = CreateRoomForm()
    join_form = JoinRoomForm()
    if create_form.validate_on_submit():
        room = Room(name=create_form.room_name.data)
        room.generate_code()
        db.session.add(room)
        db.session.commit()
        flash(f'Room {room.name} created.')
        return redirect(url_for('lobby', room_code=room.code))
    elif join_form.validate_on_submit():
        return redirect(url_for('join', room_code=join_form.room_code.data))
    return render_template('index.html', title='Questionable', create_form=create_form, join_form=join_form)


@app.route('/lobby/<room_code>')
def lobby(room_code):
    room = Room.query.filter_by(code=room_code).first_or_404()
    return render_template('lobby.html', title=f'{room.name}', room=room)


@app.route('/join/<room_code>', methods=['GET', 'POST'])
def join(room_code):
    room = Room.query.filter_by(code=room_code).first_or_404()
    new_user_form = NewUserForm()
    if new_user_form.validate_on_submit():
        user = User(name=new_user_form.name.data, room_code=room_code)
        db.session.commit()
        login_user(user)
        flash(f"Joined {room.name}")
        return redirect(url_for('member_view', room_code=room.code))
    return render_template('join.html', title='Join room', room=room, form=new_user_form)


@app.route('/member_view/<room_code>')
def member_view(room_code):
    room = Room.query.filter_by(code=room_code).first_or_404()
    return render_template('member_view.html', title='Viewing room', room=room)


@app.route('/refresh_users', methods=['POST'])
def refresh_users():
    room_code = request.form['code']
    room = Room.query.filter_by(code=room_code).first()
    users = {}
    all_ready = True
    for user in room.users:
        users[user.name] = {'is_ready': user.is_ready, 'score': user.score}
        if user.is_ready is False:
            all_ready = False
    return jsonify({'users': users, 'all_ready': all_ready})


@app.route('/user_ready', methods=['POST'])
def user_ready():
    user_id = request.form['user_id']
    user = User.query.get(int(user_id))
    user.is_ready = True
    db.session.commit()
    return jsonify({})


@app.route('/about')
def about():
    return render_template('about.html', title='About')