from smarts.core.utils.sumo import sumolib, traci, SUMO_PATH

PORT = 8001


def connect(port, order=None):
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


if __name__ == "__main__":
    client = connect(PORT, 2)

    test_client_connection(client, "Ext client")
