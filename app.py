import os

import flask

app = flask.Flask('AIforcesJudge')


# @app.before_first_request
# def startup():
#
#     if os.path.exists('startup.lock'):
#         return
#
#     if os.path.exists('tmp'):
#         os.remove('tmp')
#
#     os.mkdir('tmp')
#
#     app.logger.info("startup done")


@app.route('/judge', methods=['POST'])
def judge():
    data = flask.request.get_json(force=True)
    app.mp_queue.put(data)
    return "", 200



