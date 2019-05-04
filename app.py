import os

from flask import Flask
from flask import request, jsonify


app = Flask('AIforcesJudge')


@app.before_first_request
def startup():

    if os.path.exists('startup.lock'):
        return

    if not os.path.exists('tmp'):
        os.mkdir('tmp')

    for folder in os.listdir('tmp'):
        os.removedirs(folder)

    app.logger.info("startup done")


@app.route('/judge', methods=['POST'])
def judge():
    data = request.get_json(force=True)
    print(data)
    return jsonify({
        "query_id": data["query_id"],
        "player_1_verdict": "OK",
        "player_2_verdict": "ML",
        "winner": "player_1",
        "log": [
            [0, 0, 0],
            [0, 0, 1],
            [0, 1, 1],
            [1, 1, 1]
        ]
    })



