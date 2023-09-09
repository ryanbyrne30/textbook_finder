import json
import requests
import os

session = requests.Session()
session.headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 12; Pixel 6 Build/SD1A.210817.023; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36",
    "Accept": "*/*",
    "Connection": "keep-alive",
}

cur_file = os.path.abspath(__file__)
cur_dir = "/".join(cur_file.split("/")[:-1])


def save_data(data, filename):
    dest = f"{cur_dir}/data/{filename}"
    with open(dest, "w") as f:
        json.dump(data, f, indent=2)
    return dest


def read_data(filename):
    target = f"{cur_dir}/data/{filename}"
    with open(target, "r") as f:
        return json.load(f)
