import time
import threading

import requests

from smarts.core.utils.sumo import traci


service_port = 8888
sumo_port = 8001

client = None


def connect(port, order=None):
    time.sleep(1)
    traci_conn = traci.connect(port, numRetries=100, proc=None, waitBetweenRetries=0.1)
    if order is not None:
        traci_conn.setOrder(order)
    return traci_conn


def test_client_connection(client, client_name):
    for i in range(10):
        print(f"{client_name} steping simulation {i}")
        client.simulationStep()

    client.close()
    print("client closed")


def send_request(end_point, payload=None, port=service_port):
    requests.get(f"http://localhost:{port}/{end_point}", params=payload)


def main(times=3, with_ext_client=False):
    setup()
    while times > 0:
        time.sleep(1)
        start()
        time.sleep(3)
        stop()
        time.sleep(1)
        reset()
        times -= 1


def setup():
    payload = {"scenario": "scenarios/kyber"}
    send_request("setup", payload=payload)


def reset():
    send_request("reset")


def start():
    send_request("start")


def stop():
    send_request("stop")


if __name__ == "__main__":
    main(times=3)
