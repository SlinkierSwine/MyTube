"""API работы с пользователем"""
import re
from flask import jsonify, request
from data.models.user import User
from data import db_session
from flask_restful import Resource, abort
from flask_login import login_user


def valid_email(email):
    """Проверка правильности введенного email"""
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if re.search(regex, email):
        return True
    return False


class RegisterResource(Resource):
    """Ресурс для регистрации пользователя"""
    def post(self):
        db_sess = db_session.create_session()
        username = request.args.get('username')
        password = request.args.get('password')
        email = request.args.get('email')
        if username is None or password is None or email is None:
            abort(400, message='Missing arguments. You have to pass username, password and email')
        if not valid_email(email):
            abort(400, message='Invalid email')
        if db_sess.query(User).filter(User.email == email).first():
            abort(400, message='User already registered')
        user = User(name=username, email=email)
        user.set_password(password)
        db_sess.add(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class LoginResource(Resource):
    """Ресурс для входа в аккаунт"""
    def post(self):
        db_sess = db_session.create_session()
        password = request.args.get('password')
        email = request.args.get('email')
        user = db_sess.query(User).filter(User.email == email).first()
        if user and user.check_password(password):
            login_user(user)
            return jsonify({'success': 'OK'})
        abort(400, message='Invalid login or password')
