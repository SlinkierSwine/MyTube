from flask import Blueprint, abort, render_template, redirect, request
from data import db_session
from data.models.video import Video
from data.models.user import User
from data.forms import EditVideoForm, EditUserForm, EditPasswordForm
from data._secure_filename import secure_filename_w_cyrillic
from flask_login import login_required, current_user
import shutil
import os
from config import Config


account_blueprint = Blueprint(
    'account',
    __name__,
    template_folder='templates'
)


@account_blueprint.route('/<int:user_id>')
def profile(user_id):
    pathsep = os.path.sep
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        abort(404)
    else:
        if current_user.is_authenticated and current_user.id == user_id:
            videos = db_sess.query(Video).filter(Video.user_id == user_id)
        else:
            videos = db_sess.query(Video).filter(Video.user_id == user_id and Video.is_private != 1)
        return render_template('account.html', user=user, videos=videos, pathsep=pathsep, title=f'MyTube: {user.name}')


@account_blueprint.route('/delete/<int:video_id>', methods=['GET', 'POST'])
@login_required
def delete(video_id):
    db_sess = db_session.create_session()
    video = db_sess.query(Video).filter(Video.id == video_id, Video.user == current_user).first()
    if video:
        db_sess.delete(video)
        db_sess.commit()
        path = os.path.join(Config.UPLOAD_PATH,
                            str(current_user.id),
                            video.created_date.strftime('%m-%d-%Y-%H-%M-%S-%f'))
        if os.path.exists(path):
            shutil.rmtree(path)
        else:
            abort(400)
    else:
        abort(404)
    return redirect(f'/account/{str(current_user.id)}')


@account_blueprint.route('/edit/video/<int:video_id>', methods=['GET', 'POST'])
@login_required
def edit_video(video_id):
    form = EditVideoForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        video = db_sess.query(Video).filter(Video.id == video_id, Video.user == current_user).first()
        if video:
            form.title.data = video.title
            form.description.data = video.description
            form.is_private.data = video.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        video = db_sess.query(Video).filter(Video.id == video_id, Video.user == current_user).first()
        if video:

            if form.image.data.filename:
                old_preview = video.preview
                video.preview = secure_filename_w_cyrillic(form.image.data.filename)

                path_to_file = os.path.join(Config.UPLOAD_PATH,
                                            str(current_user.id),
                                            video.created_date.strftime('%m-%d-%Y-%H-%M-%S-%f'))

                image = form.image.data
                image.save(os.path.join(path_to_file, video.preview))

                os.remove(os.path.join(path_to_file, old_preview))

            video.title = form.title.data
            video.description = form.description.data
            video.is_private = form.is_private.data
            db_sess.commit()

            return redirect(f'/account/{str(current_user.id)}')
        else:
            abort(404)
    return render_template('edit_video.html',
                           title='MyTube: Редактирование видео',
                           form=form
                           )


@account_blueprint.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    form = EditUserForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == user_id).first()
        if user:
            form.name.data = user.name
            form.email.data = user.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == user_id).first()
        if user:
            user.name = form.name.data
            user.email = form.email.data
            db_sess.commit()
            return redirect(f'/account/{str(current_user.id)}')
        else:
            abort(404)
    return render_template('edit_user.html',
                           title='MyTube: Редактирование пользователя',
                           form=form
                           )


@account_blueprint.route('/edit/password/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_password(user_id):
    form = EditPasswordForm()

    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('edit_password.html', title='MyTube: Редактирование пароля',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == user_id).first()
        if user and user.check_password(form.old_password.data):
            user.set_password(form.password.data)
            db_sess.commit()
            return redirect(f'/account/{str(current_user.id)}')
        else:
            return render_template('edit_password.html', title='MyTube: Редактирование пароля',
                                   form=form,
                                   message="Неправильный пароль")
    return render_template('edit_password.html',
                           title='MyTube: Редактирование пароля',
                           form=form
                           )
