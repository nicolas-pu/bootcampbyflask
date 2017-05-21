from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import Length, Required


class AskForm(FlaskForm):
    title = StringField('Title', validators=[Required(), Length(1, 64)])
    description = TextAreaField('Description', validators=[Required()])
    tags = StringField('Tags', validators=[Required()])
    submit = SubmitField('Submit')


class AnswerForm(FlaskForm):
    question = HiddenField('Question')

    description = TextAreaField('Description', validators=[Required()])

    submit = SubmitField('Post your answer')
