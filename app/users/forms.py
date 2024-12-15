from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from flask_wtf.file import FileField, FileAllowed
from app import db
from app.users.models import User  # Імпортуємо модель користувача для перевірки унікальності email
from wtforms.validators import ValidationError

# Для хешування паролів
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), 
                                      Length(min=4, max=16), 
                                      Regexp('^[A-Za-z0-9_]+$', message="Username can only contain letters, numbers, and underscores.")])

    email = StringField('Email', 
                        validators=[DataRequired(), 
                                    Email()])
    
    password = PasswordField('Password', 
                             validators=[DataRequired(), 
                                        Length(min=6)])

    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), 
                                                EqualTo('password')])

    profile_picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])

    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already in use.')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

from wtforms import TextAreaField
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), 
                                      Length(min=4, max=16), 
                                      Regexp('^[A-Za-z0-9_]+$', message="Username can only contain letters, numbers, and underscores.")])

    email = StringField('Email', 
                        validators=[DataRequired(), 
                                    Email()])

    profile_picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])

    # Додаємо поле about_me
    about_me = TextAreaField('About Me', validators=[Length(max=500)])

    submit = SubmitField('Update')

    def __init__(self, current_user, *args, **kwargs):
        super(UpdateAccountForm, self).__init__(*args, **kwargs)
        self.current_user = current_user
        
        self.username.data = current_user.username
        self.email.data = current_user.email
        self.about_me.data = current_user.about_me  # Якщо у користувача є це поле

    def validate_email(self, email):
        """Перевірка унікальності email"""
        if email.data != self.current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is already in use.')

    def validate_username(self, username):
        """Перевірка унікальності username"""
        if username.data != self.current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is already taken.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Старий пароль', validators=[DataRequired()])
    new_password = PasswordField('Новий пароль', validators=[
        DataRequired(), Length(min=4)
    ])
    confirm_password = PasswordField('Підтвердження нового пароля', validators=[
        DataRequired(), EqualTo('new_password', message='Паролі повинні співпадати')
    ])
    submit = SubmitField('Змінити пароль')  # Додано поле submit
