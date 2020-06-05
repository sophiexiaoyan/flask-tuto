from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flaskr.config import Config

db = SQLAlchemy()

def create_app(test_config=None):
    # __name__ is the name of the current Python module
    app = Flask(__name__)

    if test_config is None:
        # read configuration from class Config
        app.config.from_object(Config)
    else:
        app.config.from_object(test_config)
    # app.config['SECRET_KEY'] = 'secret'
    # app.config['DEBUG'] = True
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost:3306/flaskr'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)

    # Import and register the blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    # the endpoint for the index view defined below will be blog.index
    # app.add_url_rule() associates the endpoint name 'index' with the / url so that
    # url_for('index') or url_for('blog.index') will both work
    app.add_url_rule('/', endpoint='index')

    # route creates a connection between the URL and a function that returns a response
    @app.route('/hello')
    def hello():
        return 'Hello World'

    return app
