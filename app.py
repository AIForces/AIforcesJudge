from flask import Flask
from flask import request, jsonify

app = Flask('AIforcesJudge')


@app.route('/judge', methods=['POST'])
def judge():
    data = request.get_json(force=True)
    print(data)
    return jsonify("ok")



