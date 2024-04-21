from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class TovarForm(FlaskForm):
    name = StringField('Название товара', validators=[DataRequired()])
    name1 = StringField('Описание товара', validators=[DataRequired()])
    name2 = StringField('Размеры товара', validators=[DataRequired()])
    name3 = StringField('Материалы товара', validators=[DataRequired()])
    prise = StringField('Материалы товара', validators=[DataRequired()])
    submit = SubmitField('Выставить на продажу')
