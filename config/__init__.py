import os
from pathlib import Path

IP = "127.0.0.1"
PORT = 3001
RESULT_ENDPOINT = "http://127.0.0.1:3000/judge/receive_data"
TRUSTED_IPS = ['127.0.0.1']
DEBUG = True
BASIC_PATH = str(Path(os.path.dirname(os.path.realpath(__file__))).parent)
