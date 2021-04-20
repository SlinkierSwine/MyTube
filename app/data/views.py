from application import app, login_manager
from flask import render_template, redirect, abort, request, url_for, flash
import os
from data.forms import *
from data import db_session
from data.models.user import User
from data.models.video import Video
from flask_login import login_user, logout_user, login_required, current_user
from data._secure_filename import secure_filename_w_cyrillic
import datetime
from sqlalchemy import func


@app.route("/")
def index():
    pathsep = os.path.sep
    db_sess = db_session.create_session()
    q = request.args.get('search')
    if q:
        videos = db_sess.query(Video).filter(
            func.lower(Video.title).contains(q.lower()) |
            func.lower(Video.description).contains(q.lower())
        )
        h = f'Результат запроса: {q}'
        flash('Gfd')
    else:
        videos = db_sess.query(Video).filter(Video.is_private != 1).order_by(func.random()).limit(10)
        h = 'Видео'
    return render_template('index.html', videos=videos, h=h, pathsep=pathsep, title='MyTube')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='MyTube: Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='MyTube: Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='MyTube: Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form,
                               title='MyTube: Авторизация')
    return render_template('login.html', title='MyTube: Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    form = VideoForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()

        video = Video()
        video.title = form.title.data
        video.preview = secure_filename_w_cyrillic(form.image.data.filename)
        video.description = form.description.data
        video.file_name = secure_filename_w_cyrillic(form.content.data.filename)
        video.is_private = form.is_private.data
        created_date = datetime.datetime.now()
        video.created_date = created_date

        current_user.videos.append(video)
        db_sess.merge(current_user)
        db_sess.commit()

        path = os.path.join(app.config['UPLOAD_PATH'], str(current_user.id))
        path_to_file = os.path.join(path, created_date.strftime('%m-%d-%Y-%H-%M-%S-%f'))
        if os.path.isdir(path):
            os.mkdir(path_to_file)
        else:
            os.makedirs(path_to_file)

        videofile = form.content.data
        videofile.save(os.path.join(path_to_file, video.file_name))

        image = form.image.data
        image.save(os.path.join(path_to_file, video.preview))

        return redirect('/')
    return render_template('videos.html', title='MyTube: Добавление видео',
                           form=form)

