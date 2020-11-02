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


def loop(times=3, with_ext_client=False):
    if not with_ext_client:
        while times > 0:
            reset()
            time.sleep(3)
            start()
            time.sleep(10)
            stop()
            time.sleep(3)
            times -= 1
    else:
        while times > 0:
            t = threading.Thread(target=connect, args=(sumo_port, 2,))
            t.start()
            reset()
            t.join()
            time.sleep(1)
            start()
            test_client_connection(client, "Ext client")
            time.sleep(2)
            stop()
            times -= 1


def reset():
    payload = {"scenario": "scenarios/loop", "agent": "laner"}
    send_request("setup", payload=payload)


def start():
    send_request("start")


def stop():
    send_request("stop")


if __name__ == "__main__":
    loop(3)
