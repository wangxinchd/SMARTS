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


@dataclass
class Agents:
    name: str
    agent_specs: Dict[str, AgentSpec]

    def __post_init__(self):
        self.agents = {
            agent_id: agent_spec.build_agent()
            for agent_id, agent_spec in self.agent_specs.items()
        }


AgentOptions = {"laner": Agents("laner", agent_specs=laner_agent_specs)}


class SmartsManager:
    def __init__(self):
        self.timestep_sec = 0.1
        self.sumo_port = 8001
        self._current_agent = Agents(name="", agent_specs={})
        self._smarts = None

    def setup(self, scenario, agent):
        if self._smarts is None:
            self.init_smarts(agent)

        if self._current_agent.name != agent:
            self.reset_agent(agent)

        scenarios_iterator = Scenario.scenario_variations(
            [scenario], list(self._current_agent.agent_specs.keys()),
        )

        scenario = next(scenarios_iterator)
        self._smarts.reset(scenario)

    def reset_agent(self, agent):
        # TODO: hard-coded for now, choose a agent
        self._current_agent = AgentOptions["laner"]

    def init_smarts(self, agent):
        self.reset_agent(agent)

        agent_interfaces = {
            agent_id: agent.interface
            for agent_id, agent in self._current_agent.agent_specs.items()
        }

        self._smarts = SMARTS(
            agent_interfaces=agent_interfaces,
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
            observations = {}
            while not self._has_stopped:
                actions = {
                    agent_id: self._current_agent.agents[agent_id].act(agent_obs)
                    for agent_id, agent_obs in observations.items()
                }
                observations, _, _, _ = self._smarts.step(actions)

        self._has_stopped = False
        t = threading.Thread(target=start_stepping)
        t.start()

    def stop(self):
        self._has_stopped = True

    @property
    def smarts(self):
        return self._smarts


manager = SmartsManager()


class ResetHandler(tornado.web.RequestHandler):
    def get(self):
        scenario = self.get_argument("scenario")
        agent = self.get_argument("agent")
        manager.setup(scenario, agent)
        self.write(f"Scenario reset to {scenario.name}")


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
        [(r"/setup", ResetHandler), (r"/start", StartHandler), (r"/stop", StopHandler),]
    )


def run(port, sumo_port=8001):
    app = make_app()
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    run(port=8888)
