import pickle
import subprocess
import tempfile
import threading
from pathlib import Path
from dataclasses import dataclass
from typing import Dict

import tornado.ioloop
import tornado.web

from smarts.core.scenario import Scenario
from smarts.core.smarts import SMARTS
from smarts.core.sumo_traffic_simulation import SumoTrafficSimulation
from smarts.sstudio.types import SocialAgentActor

laner_agent = SocialAgentActor(
    name="keep-lane-agent", agent_locator="zoo.policies:keep-lane-agent-v0",
)

non_interactive_agent = SocialAgentActor(
    name=f"non-interactive-agent",
    agent_locator="zoo.policies:non-interactive-agent-v0",
    policy_kwargs={"speed": 10},
)

open_agent = SocialAgentActor(
    name="open-agent", agent_locator="zoo.policies.open-agent.open_agent:open_agent-v0"
)


AGENTS = {
    "laner": laner_agent,
    "npc": non_interactive_agent,
    "open": open_agent,
}


def build_scenario(actors, scenario_path):
    with tempfile.NamedTemporaryFile(mode="wb") as f:
        pickle.dump(actors, f)
        f.flush()
        agent_path = Path(f.name).absolute()

        try:
            subprocess.run(
                [f"SOCIAL_AGENT_PATH={agent_path} scl scenario build {scenario_path}"],
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        except Exception as e:
            print(e)


class SmartsManager:
    def __init__(self):
        self.timestep_sec = 0.1
        self.sumo_port = 8001
        self._smarts = None

    def setup(self, scenario, agents):
        if self._smarts is None:
            self.init_smarts()

        actors = []
        for agent in agents:
            actors.append(AGENTS[agent])

        build_scenario(actors, scenario)

        scenarios_iterator = Scenario.scenario_variations([scenario], [])
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
        agents = self.get_argument("agents", "").split(",")
        manager.setup(scenario, agents)
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
