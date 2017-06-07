from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_moment import Moment
from flask_pagedown import PageDown
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
db = SQLAlchemy()
bootstrap = Bootstrap()
moment = Moment()
login_manager = LoginManager()
login_manager.session_pretection = 'strong'
login_manager.login_view = 'auth.login'
pagedown = PageDown()
admin = Admin()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    moment.init_app(app)
    bootstrap.init_app(app)
    config[config_name].init_app(app)
    login_manager.init_app(app)
    admin.init_app(app)
    from .models import Article
    from .models import Question
    admin.add_view(ModelView(Article, db.session))
    admin.add_view(ModelView(Question, db.session))

    from .auth import auth as auth_blueprint
    from .feeds import feeds as feeds_blueprint
    from .main import main as main_blueprint
    from .articles import articles as articles_blueprint
    from .questions import questions as questions_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(feeds_blueprint)
    app.register_blueprint(articles_blueprint)
    app.register_blueprint(questions_blueprint)

    return app

