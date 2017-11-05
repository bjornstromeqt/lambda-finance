
# Manage database
# https://github.com/miguelgrinberg/Flask-Migrate

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from src.shared_models import db
from src import create_app
from config import DevelopmentConfig


app = create_app(DevelopmentConfig)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()

