import time
import threading

import requests

from smarts.core.utils.sumo import traci


service_port = 8888
sumo_port = 8001


def send_request(end_point, payload=None, port=service_port):
    requests.get(f"http://localhost:{port}/{end_point}", params=payload)


def main(times=3, with_ext_client=False):
    setup()
    print("setup")
    while times > 0:
        time.sleep(1)
        start()
        print("start")
        time.sleep(5)
        stop()
        print("stop")
        time.sleep(1)
        reset()
        print("reset")
        times -= 1


def setup():
    payload = {"scenario": "scenarios/kyber", "agents": "laner,open"}
    send_request("setup", payload=payload)


def reset():
    send_request("reset")


def start():
    send_request("start")


def stop():
    send_request("stop")


if __name__ == "__main__":
    main(times=3)
