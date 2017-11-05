import argparse

from flask import Flask

import config
from src.shared_models import db


class ConfirmAction(argparse.Action):
    YES = 'Y'
    NO = 'N'

    def __call__(self, parser, namespace, value, option_string=None):
        self.validate(parser, value)
        setattr(namespace, self.dest, value)

    @classmethod
    def validate(cls, parser, value):
        if value not in (cls.YES, cls.NO):
            parser.error('{} not valid choice'.format(value))


def reset_environment():
    """ Reset development environment """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config.DevelopmentConfig)
    db.app = app
    db.init_app(app)

    reset_database(db)
    add_mock_data(db)
    raise SystemExit


def reset_database(db_instance):
    print("Resetting database, erasing all data…")
    db_instance.reflect(bind=None)
    db_instance.drop_all(bind=None)
    db_instance.create_all(bind=None)
    print("Done ✅")


def add_mock_data(db_instance):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--confirm', action=ConfirmAction)
    args = parser.parse_args()
    if args.confirm is None:
        args.confirm = input('THIS ACTION WILL RESET DATABASE. ARE YOU SURE? [Y/N]: ')
        ConfirmAction.validate(parser, args.confirm)

    if args.confirm == ConfirmAction.YES:
        print('*------- RESETTING DATABASE -------*')
        reset_environment()
    elif args.confirm == ConfirmAction.NO:
        print("Skipping")
