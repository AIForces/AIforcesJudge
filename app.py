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

    app.mp_queue.put(data)
    return "", 200

