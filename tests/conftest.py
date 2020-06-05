import pytest
from flaskr import create_app, db
from flaskr.models import Post, User
from werkzeug.security import generate_password_hash

class TestConfig(object):
    SECRET_KEY = 'secret'
    DEBUG = True
    # TESTING tells Flask th at the app is in test mode. Flask changes some internal behavior so it’s easier to test
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost:3306/unittest'
    ENV = 'test'

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.drop_all()
        db.create_all()
        user1 = User(username='test', password=generate_password_hash('test'))
        user2 = User(username='test2', password=generate_password_hash('test2'))
        db.session.add_all([user1, user2])
        db.session.commit()
        post = Post(title='test title', body='test', created='2018-01-01 00:00:00', author_id=1)
        db.session.add(post)
        db.session.commit()
        yield app

# The client fixture calls app.test_client() with the application object created by the app fixture.
# Tests will use the client to make requests to the application without running the server.
@pytest.fixture
def client(app):
    return app.test_client()

# app.test_cli_runner() creates a runner that can call the Click commands registered with the application.
@pytest.fixture
def runner(app):
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post('/auth/login',data={'username': username, 'password': password})

    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)
