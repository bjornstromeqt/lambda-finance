
import pusher

import config


def get_client():
    pusher_client = pusher.Pusher(
        app_id=config.current_config.PUSHER_APP_ID,
        key=config.current_config.PUSHER_KEY,
        secret=config.current_config.PUSHER_SECRET,
        cluster='eu',
        ssl=True
    )
    return pusher_client


def send_notification(user, data):
    pusher_client = get_client()
    channel_name = 'private-user-{}'.format(user.id)
    event = 'notification'
    try:
        pusher_client.trigger(channel_name, event, data)
    except Exception:
        pass
