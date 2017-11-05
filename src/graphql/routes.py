import json
import six

from flask import Blueprint, request, make_response, jsonify
from graphql import Source, execute, parse, validate, error as graphql_error

from src.graphql import schema


graphql_page = Blueprint('graphql_api', __name__)


@graphql_page.route('/graphql/schema', methods=['GET'])
def graphql_get_schema():
    introspection_dict = schema.introspect()
    return json.dumps(introspection_dict)


@graphql_page.route('/graphql', methods=['POST'])
def graphql_endpoint():
    query, variables, operation_name = _get_graphql_params(request.get_json())
    source = Source(query, name='GraphQL request')

    try:
        ast = parse(source)
        validation_errors = validate(schema, ast)
        if validation_errors:
            result = {'message': 'Invalid query', 'errors': [_format_error(e) for e in validation_errors]}
            return make_response(jsonify(result), 400)
    except Exception as e:
        result = {'message': 'Error parsing query', 'errors': [str(e)]}
        return make_response(jsonify(result), 400)

    execution_result = execute(
        schema,
        ast,
        variable_values=variables,
        operation_name=operation_name
    )

    response = {}
    status_code = 200
    if execution_result.errors:
        response['errors'] = [_format_error(e) for e in execution_result.errors]
        status_code = 400
    if execution_result.data:
        response['data'] = execution_result.data

    response_string = json.dumps(response, separators=(',', ':'))
    return make_response(response_string, status_code)


def _get_graphql_params(data):
    query = data.get('query')
    variables = data.get('variables', {})
    operation_name = data.get('operationName')
    return query, variables, operation_name


def _format_error(e):
    if isinstance(e, graphql_error.GraphQLError):
        return graphql_error.format_error(e)

    return {'message': six.text_type(e)}

