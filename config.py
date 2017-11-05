current_config = None


def set_current_config(active_configuration):
    global current_config
    current_config = active_configuration


LOCAL_POSTGRES_CONNECTION = 'postgresql+psycopg2://{user}:{password}@localhost:{port}/{db}'
CLOUD_POSTGRES_CONNECTION = 'postgresql+psycopg2://{user}:{password}@/{database}?host=/cloudsql/{connection_name}'


class Config(object):
    """
    Common configurations
    """

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = False
    SECRET_KEY = '\xfd\xb41\xb6\xb6\x1c\x17\xabs\xb2G\xeaN*q6\x81*\\X\xe4t\xaf\x16'

    INTERNAL_ACCESS_SECRET_KEY = '\xa2\x03^\x8a\x94\xe2\xc1!\x0c\x85\x80\xd3\x9d\x06$\x94,\x1f\xf9\xc7\xddk\xb7F'

    GOOGLE_API_KEY = 'AIzaSyAHfI2nd3E2-qHnSCQmxgw7AaGggD6_wQk'

    INTRINIO_USERNAME = '777c68e461f14c166e98750ddb8d8faa'
    INTRINIO_PASSWORD = 'c043e7334f2ee664eac8cd7b6a23fc26'

    PUSHER_APP_ID = '402008'
    PUSHER_KEY = 'a742082876705ec3a841'
    PUSHER_SECRET = '268500e79002559913a0'

    CLOUD_SQL_PASSWORD = 'iy5qej1ua6rJ2jva'
    DB_PORT = 5432

    PORT = 9999

    INFLUX_USER = 'admin'
    INFLUX_PASSWORD = 'C7HHS1BwuSNCKABq'
    INFLUX_HOST = '35.189.206.114'
    INFLUX_PORT = 8086
    INFLUX_DB = 'stock'


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    _dev_postgres_backend = LOCAL_POSTGRES_CONNECTION.format(
        user='postgres',
        password=Config.CLOUD_SQL_PASSWORD,
        port=Config.DB_PORT,
        db='lambda',
    )

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = str(_dev_postgres_backend)


class ProductionConfig(Config):
    """
    Production configuration
    """
    _prod_postgres_backend = CLOUD_POSTGRES_CONNECTION.format(
        user='postgres',
        password=Config.CLOUD_SQL_PASSWORD,
        database='lambda',
        connection_name='lambda-182214:europe-west1:lambda-master'
    )
    SQLALCHEMY_DATABASE_URI = _prod_postgres_backend


class TestingConfig(Config):
    """
    Development configurations
    """
    _testing_postgres_backend = LOCAL_POSTGRES_CONNECTION.format(
        user='postgres',
        password='',
        port=Config.DB_PORT,
        db='lambda_test',
    )

    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = _testing_postgres_backend
