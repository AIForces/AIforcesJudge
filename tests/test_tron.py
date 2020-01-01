import requests as rq

point = "http://127.0.0.1:3001/judge"
sol = open("player.cpp").read()

if __name__ == '__main__':
    rq.post(point, json={
        "invocation_id": 0,
        "problem": "tron",
        "solutions": [
            {
                "source": sol,
                "lang": "g++17"
            },
            {
                "source": sol,
                "lang": "g++17"
            }
        ],
        "tests": [1]
    })
