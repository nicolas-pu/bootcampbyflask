import os

class Config:
    SECRET_KEY = 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    #SQLALCHEMY_TRACK_MODIFICATIONS = True
    #SQLALCHEMY_RECORD_QUERIES = True
    

    @staticmethod
    def init_app(app):
        pass



class DevelopmentConfig(Config):
    DEBUT = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/bootcampbyflask'



config = {
        'default': DevelopmentConfig
        }
