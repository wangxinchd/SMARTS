import threading

import tornado.ioloop
import tornado.web

from smarts.core.agent import AgentSpec, AgentPolicy
from smarts.core.agent_interface import AgentInterface, AgentType
from smarts.core.scenario import Scenario
from smarts.core.smarts import SMARTS
from smarts.core.sumo_traffic_simulation import SumoTrafficSimulation


AGENT_ID = "Agent-007"


class Policy(AgentPolicy):
    def act(self, obs):
        return "keep_lane"


timestep_sec = 0.1
sumo_port = 8001
scenarios = ["scenarios/loop"]
agent_spec = AgentSpec(
    interface=AgentInterface.from_type(AgentType.Laner, max_episode_steps=100000),
    policy_builder=Policy,
)
agent_specs = {AGENT_ID: agent_spec}
agent_interfaces = {
    agent_id: agent.interface for agent_id, agent in agent_specs.items()
}

scenarios_iterator = Scenario.scenario_variations(scenarios, list(agent_specs.keys()),)

s = SMARTS(
    agent_interfaces=agent_interfaces,
    traffic_sim=SumoTrafficSimulation(
        headless=False,
        time_resolution=timestep_sec,
        num_external_sumo_clients=0,
        sumo_port=sumo_port,
        auto_start=True,
    ),
    timestep_sec=timestep_sec,
)

agent = agent_spec.build_agent()
stop = False


class ResetHandler(tornado.web.RequestHandler):
    def get(self):
        scenario = next(scenarios_iterator)
        s.reset(scenario)
        self.write(f"Scenario reset to {scenario.name}")


class StartHandler(tornado.web.RequestHandler):
    def get(self):
        def start_stepping():
            observations = {}
            while not stop:
                agent_obs = observations.get(AGENT_ID)
                agent_action = agent.act(agent_obs)
                observations, _, _, _ = s.step({AGENT_ID: agent_action})

        global stop
        stop = False
        t = threading.Thread(target=start_stepping)
        t.start()
        self.write("Scenario is running!")


class StopHandler(tornado.web.RequestHandler):
    def get(self):
        global stop
        stop = True
        self.write("Scenario stopped!")


def make_app():
    return tornado.web.Application(
        [(r"/reset", ResetHandler), (r"/start", StartHandler), (r"/stop", StopHandler),]
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
