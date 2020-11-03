import threading
from dataclasses import dataclass
from typing import Dict

import tornado.ioloop
import tornado.web

from smarts.core.agent import AgentSpec
from smarts.core.scenario import Scenario
from smarts.core.smarts import SMARTS
from smarts.core.sumo_traffic_simulation import SumoTrafficSimulation
from smarts.service.agents.laner import agent_specs as laner_agent_specs


class SmartsManager:
    def __init__(self):
        self.timestep_sec = 0.1
        self.sumo_port = 8001
        self._smarts = None

    def setup(self, scenario):
        if self._smarts is None:
            self.init_smarts()

        scenarios_iterator = Scenario.scenario_variations([scenario], [],)
        self._scenarios_iterator = scenarios_iterator

        scenario = next(self._scenarios_iterator)
        self._smarts.reset(scenario)

    def reset(self):
        scenario = next(self._scenarios_iterator)
        self._smarts.reset(scenario)

    def init_smarts(self):
        self._smarts = SMARTS(
            agent_interfaces={},
            traffic_sim=SumoTrafficSimulation(
                headless=False,
                time_resolution=self.timestep_sec,
                num_external_sumo_clients=0,
                sumo_port=self.sumo_port,
                auto_start=True,
            ),
            timestep_sec=self.timestep_sec,
        )
        self._has_stopped = False

    def start(self):
        def start_stepping():
            while not self._has_stopped:
                self._smarts.step({})

        self._has_stopped = False
        t = threading.Thread(target=start_stepping)
        t.start()

    def stop(self):
        self._has_stopped = True

    @property
    def smarts(self):
        return self._smarts


manager = SmartsManager()


class SetupHandler(tornado.web.RequestHandler):
    def get(self):
        scenario = self.get_argument("scenario")
        manager.setup(scenario)
        self.write(f"Scenario setup to {scenario}")


class ResetHandler(tornado.web.RequestHandler):
    def get(self):
        manager.reset()
        self.write(f"Scenario reset.")


class StartHandler(tornado.web.RequestHandler):
    def get(self):
        manager.start()
        self.write("Scenario is running!")


class StopHandler(tornado.web.RequestHandler):
    def get(self):
        manager.stop()
        self.write("Scenario stopped!")


def make_app():
    return tornado.web.Application(
        [
            (r"/setup", SetupHandler),
            (r"/reset", ResetHandler),
            (r"/start", StartHandler),
            (r"/stop", StopHandler),
        ]
    )


def run(port, sumo_port=8001):
    app = make_app()
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    run(port=8888)
