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
    if not all(item in data for item in ['game', 'lang', 'source', 'timeout', 'challenge_id', 'state_par']):
        return "", 400

    app.mp_queue.put(data)
    return "", 200

# 1) POST /addState
# 2) DELETE /destroyState
# 3) DELETE /destroyAll


@app.route('/addState', methods=['POST'])
@check_access
def add_state():

    if flask.request.remote_addr not in config.TRUSTED_IPS:
        return '', 403

    game, file = tuple(flask.request.files.items(), )[0]
    file.save(f'states/{game}_state.py')

    app.mp_queue.put('REIMPORT_STATES')

    return '', 200


@app.route('/deleteState', methods=['DELETE'])
@check_access
def delete_state():

    file = flask.request.args.get('game')
    if not file:
        return '', 400

    Path(f'states/{file}_state.py').unlink()
    return '', 200


@app.route('/deleteAll', methods=['DELETE'])
@check_access
def delete_all():
    states = [state for state in Path('states').iterdir() if not state.name.startswith(('base', '__'))]
    for state in states:
        state.unlink()

    return '', 200
