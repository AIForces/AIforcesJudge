import functools
import os
from pathlib import Path

import flask
import config


app = flask.Flask('AIforcesJudge')


def check_access(f):

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if flask.request.remote_addr not in config.TRUSTED_IPS:
            return "", 403

        return f(*args, **kwargs)
    return wrapper


@app.route('/judge', methods=['POST', ])
@check_access
def judge():
    """
    Entry point from web
    :return:
    """

    data: dict = flask.request.get_json(force=True)
    if not all(item in data for item in ['invocation_id', 'problem', 'solutions', 'tests']):
        return "", 400

    app.mp_queue.put(data)
    return "", 200
