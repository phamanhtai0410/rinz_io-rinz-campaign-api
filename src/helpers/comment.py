# -*- coding: utf-8 -*-
"""
    Utils has nothing to do with models and views.
"""
import json
import traceback
import requests
from src.constants import AppConstants
from sentry_sdk import capture_exception
from src.config import DefaultConfig


def log_any(x, *args, **kwargs):
    """
        Log any message to json format.
    """
    msg = {
        'msg': x,
    }

    print()
    if args:
        msg['args'] = json.dumps(args)
    if kwargs:
        msg['kwargs'] = json.dumps(kwargs)
    print(msg)
    return json.dumps(msg)


def send_message_socket(message_type, item_type, author_user, item_id, comment_payload):
    """Call Websocket service to deliver a message"""
    _payload = {
        "to_room": '{}:{}'.format(item_type, item_id),
        "from_service": "comment",
        "type": message_type,
        "payload": comment_payload
    }
    try:
        resp = requests.post('{}/iapi/hooks/send_message'.format(DefaultConfig.SOCKET_SERVER_DOMAIN),
                             json=_payload,
                             verify=False,
                             timeout=5)
        log_any('Call Socket service resp code', resp.status_code, resp.text)
    except Exception as e:
        traceback.print_exc(e)
        capture_exception(e)
