from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, TextAreaField, StringField, FileField
from wtforms.validators import DataRequired, InputRequired
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileAllowed


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
    image = FileField('Превью',
                      validators=[InputRequired(), FileAllowed(['jpg', 'png'], 'Только изображения формата .jpg и .png')])
    content = FileField('Видео',
                        validators=[InputRequired(), FileAllowed(['mp4', 'avi'], 'Только видео формата .mp4 и .avi')])
    is_private = BooleanField('Приватное')
    submit = SubmitField('Загрузить')


class EditVideoForm(FlaskForm):
    title = TextAreaField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание')
    image = FileField('Превью',
                      validators=[FileAllowed(['jpg', 'png'], 'Только изображения формата .jpg и .png')])
    is_private = BooleanField('Приватное')
    submit = SubmitField('Изменить')


class EditUserForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    submit = SubmitField('Изменить данные')


class EditPasswordForm(FlaskForm):
    old_password = PasswordField('Старый пароль', validators=[DataRequired()])
    password = PasswordField('Новый пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите новый пароль', validators=[DataRequired()])
    submit = SubmitField('Изменить пароль')
