from application import app, login_manager
from flask import render_template, redirect, abort
import os
from data.forms import *
from data import db_session
from data.models.user import User
from data.models.video import Video
from flask_login import login_user, logout_user, login_required, current_user
from data._secure_filename import secure_filename_w_cyrillic
import datetime


@app.route("/")
def index():
    db_sess = db_session.create_session()
    videos = db_sess.query(Video).filter(Video.is_private is not True)
    return render_template('index.html', videos=videos)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
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
    return render_template('register.html', title='Регистрация', form=form)


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
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


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
    return render_template('videos.html', title='Добавление видео',
                           form=form)


@app.route('/watch/<int:video_id>')
def show_video(video_id):
    db_sess = db_session.create_session()
    video = db_sess.query(Video).get(video_id)
    author = db_sess.query(User).get(video.user_id)
    if not video:
        abort(404)
    else:
        return render_template('player.html', video=video, author=author)


@app.route('/profile/<int:user_id>')
def profile(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    videos = db_sess.query(Video).filter(Video.user_id == user_id)
    return render_template('profile.html', user=user, videos=videos)