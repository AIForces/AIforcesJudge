import multiprocessing as mp
import requests as rq


def run(queue: mp.Queue):
    data = queue.get()
    rq.post("http://localhost:3001/receive_data", json=data)
