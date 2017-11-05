
import json
from flask import Blueprint, request, make_response,jsonify

from src import pusher_api

pusher_page = Blueprint('pusher_api', __name__, url_prefix='/pusher')


@pusher_page.route('/auth/jsonp', methods=['GET'])
def pusher_authentication():
    """
    Authenticate to private channel.

    The private channel have the form 'private-user-<user_id>'

    A user must be authenticated to be able to subscribe to it's private channel.
    :return:
    """
    # Pusher JS-client don't support sending data in headers when authenticating with jsonp,
    # therefore, token is sent as query-argument
    token = request.args.get('token')
    '''
    user = User.verify_auth_token(token)
    if not user:
        return make_response(jsonify({'message': 'Invalid token'}), 401)
    '''

    # See if channel name matches user_id.
    # Channel name should be on the form: 'private-user-<user_id>'
    channel_name = request.args['channel_name']
    try:
        user_id_from_channel = int(channel_name.split('-')[2])
        # assert user_id_from_channel == user.id
    except (ValueError, IndexError):
        return make_response(jsonify({'message': 'Invalid channel name <{}>'.format(channel_name)}), 400)
    except AssertionError:
        return make_response(jsonify({'message': 'Not authorized for the requested channel'}), 403)

    # Authenticate with socket_id and callback,
    # see docs: https://pusher.com/docs/authenticating_users
    socket_id = request.args['socket_id']
    callback = request.args['callback']

    pusher_client = pusher_api.get_client()
    auth = pusher_client.authenticate(channel=channel_name, socket_id=socket_id)

    text = '{}({})'.format(callback, json.dumps(auth))
    response = make_response(text, 200)
    response.headers['Content-Type'] = 'application/javascript'
    return response
