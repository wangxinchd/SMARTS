from smarts.core.utils.sumo import traci


def connect(port, order=None):
    traci_conn = traci.connect(port, numRetries=100, proc=None, waitBetweenRetries=0.1)
    if order is not None:
        traci_conn.setOrder(order)
    return traci_conn



if __name__ == "__main__":
    cli = connect(8001, order=2)
    while True:
        cli.simulationStep()