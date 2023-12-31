# -*- coding: utf-8 -*-

# Стандартные библиотеки Python

# Библиотеки третьей стороны
from flask_babel import lazy_gettext as _loc
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

# Собственные модули
from app.models import User


class LoginForm(FlaskForm):
    """
    Класс формы для входа пользователя.

    Attributes:
        username (StringField): Поле для ввода имени пользователя.
        password (PasswordField): Поле для ввода пароля.
        remember_me (BooleanField): Флажок "Запомнить меня".
        submit (SubmitField): Кнопка "Войти".
    """
    username: StringField = StringField(_loc('Имя пользователя'), validators=[DataRequired()])
    password: PasswordField = PasswordField(_loc('Пароль'), validators=[DataRequired()])
    remember_me: BooleanField = BooleanField(_loc('Запомни меня'))
    submit: SubmitField = SubmitField(_loc('Войти'))


class RegistrationForm(FlaskForm):
    """
    Класс формы регистрации пользователя.

    Attributes:
        username (StringField): Поле для ввода имени пользователя.
        email (StringField): Поле для ввода почты.
        password (PasswordField): Поле для ввода пароля.
        password2 (PasswordField): Поле для повторного ввода пароля.
        submit (SubmitField): Кнопка "Регистрация".
    """
    username: StringField = StringField(_loc('Имя пользователя'), validators=[DataRequired()])
    email: StringField = StringField(_loc('Почта'), validators=[DataRequired(), Email()])
    password: PasswordField = PasswordField(_loc('Пароль'), validators=[DataRequired()])
    password2: PasswordField = PasswordField(_loc('Повтор пароля'),
                                             validators=[DataRequired(), EqualTo('password')])
    submit: SubmitField = SubmitField(_loc('Регистрация'))

    def validate_username(self, username):
        """
        Проверяет уникальность имени пользователя.

        Args:
            username (StringField): Поле имени пользователя.

        Raises:
            ValidationError: Если имя пользователя уже занято.
        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_loc('Используйте другое имя.'))

    def validate_email(self, email):
        """
        Проверяет уникальность почты.

        Args:
            email (StringField): Поле почты.

        Raises:
            ValidationError: Если почта уже используется другим пользователем.
        """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_loc('Используйте другую почту.'))


class ResetPasswordRequestForm(FlaskForm):
    """
    Форма запроса сброса пароля.

    Attributes:
        email (StringField): Поле для ввода email-адреса пользователя. Обязательное поле.
        submit (SubmitField): Кнопка для отправки запроса сброса пароля.
    """
    email = StringField(_loc('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_loc('Запрос сброса пароля'))


class ResetPasswordForm(FlaskForm):
    """
    Форма для сброса пароля пользователя.

    Attributes:
        password (PasswordField): Поле для ввода нового пароля.
        password2 (PasswordField): Поле для повторного ввода пароля с проверкой на совпадение.
        submit (SubmitField): Кнопка для отправки запроса сброса пароля.

    """
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(_loc(
        'Повторите пароль'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_loc('Запрос сброса пароля'))
