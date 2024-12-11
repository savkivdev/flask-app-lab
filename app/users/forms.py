from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from flask_wtf.file import FileField
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

    profile_picture = FileField('Profile Picture')

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