from flask import render_template, redirect, url_for, flash, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from .forms import LoginForm, RegisterForm, ChangePasswordForm, ChangeEmailForm
from . import auth
from ..models import User, Feed
from .. import db

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('auth.index'))
        flash('Invalid email or password')
    
    return render_template('login.html', form=form)



@auth.route('/')
def index():
    return render_template('index.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()  
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data) 
        welcome_post = '{0} has joined the network,'.format(user.username, user.username)
        feed = Feed(user=user, post=welcome_post)
        db.session.add(user)
        db.session.add(feed)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))



@auth.route('/changepassword', methods=['GET', 'POST'])
@login_required
def changepassword():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.new_password.data
            db.session.add(current_user)
            flash('You have changed your password Successfully!.')
            return redirect(url_for('auth.changepassword'))
        else:
            flash('Invalid password')
    
    return render_template('auth/changepassword.html', form=form)


@auth.route('/changeemail', methods=['GET', 'POST'])
@login_required
def changeemail():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.email == form.old_email.data:
            current_user.email = form.new_email.data
            db.session.add(current_user)
            flash('You have changed your email successfully!')

        else:
            flash('Invalid email')
    return render_template('auth/changeemail.html', form=form)
