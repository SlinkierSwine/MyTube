from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, TextAreaField, StringField, FileField
from wtforms.validators import DataRequired, InputRequired
from wtforms.fields.html5 import EmailField


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться и Войти')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class VideoForm(FlaskForm):
    title = TextAreaField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание')
    image = FileField('Превью', validators=[InputRequired()])
    content = FileField('Видео', validators=[InputRequired()])
    is_private = BooleanField('Приватное')
    submit = SubmitField('Загрузить')
