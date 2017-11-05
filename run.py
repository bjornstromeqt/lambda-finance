import os

from config import ProductionConfig, DevelopmentConfig
from src import create_app


def detect_environment():
    # https://cloud.google.com/appengine/docs/flexible/python/runtime
    google_appengine_version = os.getenv('GAE_VERSION', '')

    if google_appengine_version == '':
        # Running locally
        return DevelopmentConfig

    return ProductionConfig


active_configuration = detect_environment()

app = create_app(active_configuration)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=active_configuration.PORT, threaded=True)
