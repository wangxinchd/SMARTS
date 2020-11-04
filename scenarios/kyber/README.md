## Without external sumo clients

1. `python smarts/service/server.py`
2. `python tools/service_test.py`


## With external sumo clients

1. Modify `smarts/service/server.py` line 39, change `num_external_sumo_clients` to `1`.
2. `python smarts/service/server.py`
3. `python tools/service_test.py`
4. `python tools/external_sumo_client.py`