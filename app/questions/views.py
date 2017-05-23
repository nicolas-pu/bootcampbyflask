from . import questions
from flask_login import login_required, current_user
from ..models import Question, QTag, Answer, Activity
from flask import render_template, redirect, url_for, request, make_response
from .forms import AskForm, AnswerForm
from .. import db


@questions.route('/questions')
@login_required
def allquestions():
    allquestions = Question.query.order_by(Question.create_date.desc())
    
    page = request.args.get('page', 1, type=int)
    paginator = Question.query.order_by(Question.create_date).paginate(
            page, per_page=10, error_out=False
            )

    return render_template('questions/questions.html', questions=paginator.items, pagination=paginator)


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
                  


@questions.route('/questions/<id>', methods=['GET', 'POST'])
@login_required
def question(id):
    question = Question.query.filter_by(id=id).first()
    form = AnswerForm(question=question)
    if form.validate_on_submit():
        a = Answer(user=current_user, question=question, description=form.description.data)   
        db.session.add(a)
        return render_template('questions/question.html', question=question, form=AnswerForm())
    return render_template('questions/question.html', question=question, form=form)

@questions.route('/questions/answer/accept/', methods=['GET', 'POST'])
@login_required
def accept():
    form = request.form
    answer = Answer.query.filter_by(id=form['answer']).first() 
    
    question = Question.query.filter_by(id=form['question']).first()
    answer.accept()
    

    return render_template('questions/question.html', question=question, form=AnswerForm())

    
@questions.route('/questions/favorite/', methods=['GET', 'POST'])
@login_required
def favorite():
    form = request.form
    question = Question.query.filter_by(id=form['question']).first()
    activity = Activity.query.filter_by(activity_type=Activity.FAVORITE, user=current_user, question=form['question']).first()
    
    if activity:
        db.session.delete(activity)
        db.session.commit()
    else:
        activity = Activity(activity_type=Activity.FAVORITE, user=current_user, question=form['question'])
        db.session.add(activity)
        db.session.commit()
    response = make_response('{0}'.format(question.calculate_favorites()))
    return response


@questions.route('/questions/answered')
@login_required
def answered():
    allquestions = Question.query.filter_by(has_accepted_answer=True).order_by(Question.create_date.desc())
    page = request.args.get('page', 1, type=int)
    paginator = Question.query.filter_by(has_accepted_answer=True).order_by(Question.create_date.desc()).paginate(
            page, per_page=10, error_out=False
            )
    return render_template('questions/questions.html', questions=paginator.items, pagination=paginator)


@questions.route('/questions/unswered')
@login_required
def unswered():
    allquestions = Question.query.filter_by(has_accepted_answer=False).order_by(Question.create_date.desc())
    page = request.args.get('page', 1, type=int)
    paginator = Question.query.filter_by(has_accepted_answer=False).order_by(Question.create_date.desc()).paginate(
            page, per_page=10, error_out=False
            )
    return render_template('questions/questions.html', questions=paginator.items, pagination=paginator)
