from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    surname = StringField("Фамилия", validators=[DataRequired()])
    name = StringField("Имя", validators=[DataRequired()])
    age = IntegerField("Возраст", validators=[DataRequired()])
    position = StringField("Должность", validators=[DataRequired()])
    speciality = StringField("Специальность", validators=[DataRequired()])
    address = StringField("Адрес", validators=[DataRequired()])
    email = EmailField("Электронная почта", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    repeat_password = PasswordField("Повторите пароль", validators=[DataRequired()])
    submit = SubmitField("Зарегестрироваться")