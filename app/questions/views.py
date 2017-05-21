from . import questions
from flask_login import login_required, current_user
from ..models import Question, QTag
from flask import render_template, redirect, url_for
from .forms import AskForm, AnswerForm
from .. import db


@questions.route('/questions')
@login_required
def allquestions():
    allquestions = Question.query.order_by(Question.create_date.desc())

    return render_template('questions/questions.html', questions=allquestions)


@questions.route('/questions/write', methods=['GET', 'POST'])
@login_required
def write():
    form = AskForm()    
    if form.validate_on_submit():
        question = Question(title=form.title.data, description=form.title.data, user=current_user)
        question.create_tags(form.tags.data)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('questions.allquestions'))
    return render_template('questions/ask.html', form=form)
                  


@questions.route('/questions/<id>')
@login_required
def question(id):
    question = Question.query.filter_by(id=id).first()
    form = AnswerForm(question=question)
    return render_template('questions/question.html', question=question, form=form)
