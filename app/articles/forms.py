from flask_wtf import  FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, HiddenField
from wtforms.validators import Required, Length
from flask_pagedown.fields import PageDownField

class ArticleForm(FlaskForm):
    status = HiddenField('Status')
    title = StringField('Title', validators=[Required(), Length(1, 64)])
    content = PageDownField('What is on your mind?', validators=[Required()])
    tags = StringField('Tags', validators=[Required()])
