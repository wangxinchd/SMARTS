import time

import requests

port = 8888


def send_request(end_point, payload={}):
    requests.get(f"http://localhost:{port}/{end_point}", params=payload)


def loop(times=3):
    while times > 0:
        reset()
        time.sleep(1)
        start()
        time.sleep(3)
        stop()
        times -= 1


def reset():
    payload = {"scenario": "scenarios/loop", "agent": "laner"}
    send_request("setup", payload)


def start():
    send_request("start")


def stop():
    send_request("stop")


if __name__ == "__main__":
    loop(3)
