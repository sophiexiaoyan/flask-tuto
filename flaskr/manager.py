from flaskr import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flaskr.models import User, Post

app = create_app()

migrate = Migrate(app, db)
manager = Manager(app)
# add a command db in flask-script
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
