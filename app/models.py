from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from datetime import datetime
import hashlib
from flask import request


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    feeds = db.relationship('Feed', backref='user', lazy='dynamic')
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.now)
    last_seen = db.Column(db.DateTime(), default=datetime.now)
    avatar_hash = db.Column(db.String(32))
    articles = db.relationship('Article', backref='user', lazy='dynamic')
    questions = db.relationship('Question', backref='user', lazy='dynamic')
    answers = db.relationship('Answer', backref='user', lazy='dynamic')
    activitys = db.relationship('Activity', backref='user', lazy='dynamic')
    


    
    def __init__(self, **kwargs):
        if self.email is not None and  self.avatar is None:
            self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()

    @property
    def password(self):
        raise AttributeError('password is not readable attrible')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    def get_picture(self):
        no_picture = 'http://trybootcamp.vitorfs.com/static/img/user.png'
        



        return no_picture
    

    def get_screen_name(self):
        return self.username
    def __repr__(self):
        return '<User %r>' % self.username

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url, hash=hash, size=size, default=default, rating=rating)

    def ping(self):
        self.last_seen = datetime.now()
        db.session.add(self)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class Feed(db.Model):
    __tablename__ = 'feeds'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post = db.Column(db.Text())
    date = db.Column(db.DateTime, index=True, default=datetime.now)


class Article(db.Model):
    __tablename__ = 'articles'
    DRAFT = 'D'
    PUBLISHED = 'P'
    STATUS = (
            (DRAFT, 'Draft'),
            (PUBLISHED, 'Published'),
            )
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(64))
    content = db.Column(db.Text())
    status = db.Column(db.String(1), default=DRAFT)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tags = db.relationship('Tag', backref='article', lazy='dynamic')
    create_date = db.Column(db.DateTime, index=True, default=datetime.now)
    update_date = db.Column(db.DateTime, index=True)

    @staticmethod
    def get_published():
        articles = Article.query.filter_by(status=Article.PUBLISHED).order_by(Article.create_date.desc())
        return articles

    def create_tags(self, tags):
        tags = tags.strip()
        tag_list = tags.split(' ')
        for tag in tag_list:
            temp = Tag.query.filter_by(tag=tag).first()
            if temp:
                t = Tag(tag=tag, article=self)
                db.session.add(t)
            else:
                t = Tag(tag=tag, article=self)
                db.session.add(t)

    def get_tags(self):
        return self.tags

    def add_tag(self, tag):
        if self.tags:
            self.tags.append(tag)
        else:
            self.tags = tag


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(64))
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    
    def __str__(self):
        return self.tag
    
    @staticmethod
    def get_popular_tags():
        tags = Tag.query.all()
        count = {}
        for tag in tags:
            if tag.article.status == Article.PUBLISHED:
                if tag.tag in count:
                    count[tag.tag] = count[tag.tag] + 1
                else:
                    count[tag.tag] = 1
        
        sorted_count = sorted(count.items(), key=lambda t: t[1], reverse=True)
        return sorted_count[:20]


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(64))
    description = db.Column(db.String(256))
    create_date = db.Column(db.DateTime, index=True, default=datetime.now)
    update_date = db.Column(db.DateTime, index=True, default=datetime.now)
    favorites = db.Column(db.Integer, default=0)
    has_accepted_answer = db.Column(db.Boolean, default=False)
    tags = db.relationship('QTag', backref='question', lazy='dynamic')
    answers = db.relationship('Answer', backref='question', lazy='dynamic')

    def create_tags(self, tags):
        tags = tags.strip()
        tag_list = tags.split(' ')
        for tag in tag_list:
            t = QTag(tag=tag, question=self)
            db.session.add(t)

    @staticmethod
    def get_unanswered():
        return Question.query.filter_by(has_accepted_answer=False)

    @staticmethod
    def get_answered():
        return Question.query.filter_by(has_accepted_answer=True)

    def get_answers(self):
        return Answer.query.filter_by(question=self).order_by(Answer.create_date.desc())

    def get_description_preview(self):
        if len(self.description) > 255:
            return '{0}...'.format(self.description[:255])
        else:
            return self.description

    def get_tags(self):
        return self.tags

    def get_favoriters(self):
        favoriters = []
        return favoriters

    def calculate_favorites(self):
        favorites = Activity.query.filter_by(activity_type=Activity.FAVORITE, question=self.id).count()
        self.favorites = favorites
        return self.favorites
    
    def get_favoriters(self):
        favorites = Activity.query.filter_by(activity_type=Activity.FAVORITE, question=self.id)
        favoriters = []
        for favorite in favorites:
            favoriters.append(favorite.user)
        return favoriters

class QTag(db.Model):
    __tablename__ = 'qtags'
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(64))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))

    def __str__(self):
        return self.tag


class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    description = db.Column(db.String(256))
    create_date = db.Column(db.DateTime, default=datetime.now)
    update_date = db.Column(db.DateTime, index=True, default=datetime.now )
    votes = db.Column(db.Integer, default=0)
    is_accepted = db.Column(db.Boolean, default=False)

    def accept(self):
        answers = Answer.query.all()
        for answer in answers:
            answer.is_accepted = False
        self.is_accepted = True
        question = Question.query.filter_by(id=self.question_id).first()
        question.has_accepted_answer = True

class Activity(db.Model):
    __tablename__ = 'activities'
    FAVORITE = 'F'
    LIKE = 'L'
    DOWN_VOTE = 'D'
    UP_VOTE = 'U'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    activity_type = db.Column(db.String(1))
    question = db.Column(db.Integer)
    answer = db.Column(db.Integer)
