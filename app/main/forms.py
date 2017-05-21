from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required, Email, Length


class EditProfileForm(FlaskForm):
    name = StringField('Real Name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

