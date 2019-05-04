import multiprocessing as mp
import requests as rq


def run(queue: mp.Queue):
    data = queue.get()
    print(data)
    resp = {
        "query_id": 6,
        "player_1_verdict": "OK",
        "player_2_verdict": "ML",
        "winner": "player_1",
        "log": "smth"
    }
    rq.post("http://localhost:3001/receive_data", json=resp)
