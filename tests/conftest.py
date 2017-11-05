import pytest

from src import create_app
from config import TestingConfig
from src.shared_models import db as _db


# noinspection PyShadowingNames,PyUnusedLocal
@pytest.fixture(scope='session')
def app(request, autouse=True):
    """Session-wide test `Flask` application."""

    app = create_app(TestingConfig)

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


# noinspection PyShadowingNames,PyUnusedLocal
@pytest.fixture(scope='session')
def db(app, request, autouse=True):
    """Session-wide test database."""

    def teardown():
        pass

    _db.app = app
    _db.init_app(app)
    _db.drop_all(bind=None)
    _db.create_all(bind=None)

    request.addfinalizer(teardown)
    return _db


# noinspection PyShadowingNames,PyUnusedLocal
@pytest.fixture(scope='session')
def client(app, db):
    # db required as function argument to indicate fixture order for PyTest
    return app.test_client(use_cookies=False)


# noinspection PyShadowingNames
@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session

