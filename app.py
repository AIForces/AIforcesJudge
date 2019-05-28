import os

import flask
import config

app = flask.Flask('AIforcesJudge')


@app.route('/judge', methods=['POST', ])
def judge():
    """
    Entry point from web
    :return:
    """
    ip = flask.request.remote_addr

    # Trust everyone while running locally
    if config.DEBUG:
        config.RESULT_ENDPOINT = f'http:/{ip}:3000/judge/receive_data'
        config.TRUSTED_IPS.append(ip)

    if ip not in config.TRUSTED_IPS:
        return "", 403

    data: dict = flask.request.get_json(force=True)
    if not all(item in data for item in ['game', 'lang', 'source', 'timeout', 'challenge_id', 'state_par']):
        return "", 400

    app.mp_queue.put(data)
    return "", 200

