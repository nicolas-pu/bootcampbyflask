from . import main
from flask import render_template, abort, flash, redirect, url_for
from ..models import User
from .forms import EditProfileForm
from flask_login import current_user
from .. import db





@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)

    return render_template('user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm() 
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('You have been saved your profile')
        return redirect(url_for('main.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    
        
    
    return render_template('main/edit_profile.html', form=form)
