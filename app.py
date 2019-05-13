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

    # Hujak-hujak i odin thread
    from judge import Judge
    Judge(data["game"], data["lang1"], data["source1"], data["lang2"], data["source2"], 0.5, data["challenge_id"]).run()
    # app.mp_queue.put(data)
    return "", 200




