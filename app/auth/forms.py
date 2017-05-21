from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from flask_wtf import FlaskForm
from ..models import User
from wtforms import ValidationError

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')


class RegisterForm(FlaskForm):
    
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username = StringField('Username', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,'Usernames must have only letters, numbers, dots or underscores')])
    password = PasswordField('Password', validators=[Required(), EqualTo('password2', message='Passwords must math')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Register')


    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in Users,')


class ChangePasswordForm(FlaskForm):
    
    old_password = PasswordField('Old password', validators=[Required()]) 
    new_password = PasswordField('New password', validators=[Required(), EqualTo('confirm_password', message='Passwords must math')])
    confirm_password = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Submit')
 
class ChangeEmailForm(FlaskForm):

    old_email = StringField('Old email', validators=[Required(), Email()])
    new_email = StringField('New email', validators=[Required(), Email(), EqualTo('confirm_email', message='Email must math')])
    confirm_email = StringField('Confirm email', validators=[Required(), Email()])
    submit = SubmitField('Submit')

    
