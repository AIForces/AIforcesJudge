import os

import flask

app = flask.Flask('AIforcesJudge')


@app.route('/judge', methods=['POST', ])
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

