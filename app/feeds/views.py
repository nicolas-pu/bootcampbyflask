from flask import render_template
from flask import request
from ..models import User, Feed
from flask_login import login_required
from . import feeds



@feeds.route('/feeds')
def feeds():
    feeds = Feed.query.order_by(Feed.date.desc()).all()

    page = request.args.get('page', 1, type=int)
    

    pagination = Feed.query.order_by(Feed.date.desc()).paginate(
            page, per_page=10, error_out=False
            )
    
    feeds = pagination.items

    return render_template('feeds/feeds.html', feeds=pagination.items, pagination=pagination)
