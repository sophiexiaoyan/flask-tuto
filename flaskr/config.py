class Config(object):
    DEBUG = True
    SECRET_KEY = 'secret'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost:3306/flaskr'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
