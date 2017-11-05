import json

from flask import Flask, request, make_response, jsonify
from flask_graphql import GraphQLView

import config
from src.shared_models import db

# Import all models
from src.organizations.models import *


def create_app(active_config):
    """ Initiate app
    :param active_config: Configuration to use
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(active_config)

    config.set_current_config(active_config)
    if active_config is not config.TestingConfig:
        db.app = app
        db.init_app(app)

    _register_routes(app)
    _add_request_handlers(app)
    return app


def _register_routes(app):
    from src.graphql.routes import graphql_page
    from src.pusher_api.routes import pusher_page

    app.register_blueprint(pusher_page)
    app.register_blueprint(graphql_page)

    from src.graphql import schema
    app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

    from src.google_finance import historical

    @app.route('/')
    def index():
        data = historical.get_data()
        return data.to_json(orient="records")


def _add_request_handlers(app):
    @app.before_request
    def before_request():
        pass

    @app.after_request
    def add_header(response):
        response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
        response.headers['Cache-Control'] = 'public, max-age=0'
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = request.headers.get('Access-Control-Request-Headers',
                                                                               'Authorization,Set-Cookie')
        response.headers['Access-Control-Expose-Headers'] = 'Authorization,Set-Cookie'
        response.headers['Access-Control-Max-Age'] = '1'

        return response

    @app.errorhandler(404)
    def error_404(e):
        message = 'Requested URL <{}> not found'.format(request.url)
        return make_response(jsonify({'message': message, 'error': str(e)}), 404)

    @app.errorhandler(500)
    def error_500(e):
        message = 'Internal error'
        return make_response(jsonify({'message': message, 'error': str(e)}), 500)
