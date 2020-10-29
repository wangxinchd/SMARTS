import logging

from smarts.core.agent import AgentSpec, AgentPolicy
from smarts.core.agent_interface import AgentInterface, AgentType
from smarts.core.scenario import Scenario
from smarts.core.smarts import SMARTS
from smarts.core.sumo_traffic_simulation import SumoTrafficSimulation


logging.basicConfig(level=logging.INFO)

AGENT_ID = "Agent-007"


class Policy(AgentPolicy):
    def act(self, obs):
        return "keep_lane"


def main(scenarios):
    timestep_sec = 0.1
    sumo_port = 8001
    agent_spec = AgentSpec(
        interface=AgentInterface.from_type(AgentType.Laner, max_episode_steps=None),
        policy_builder=Policy,
    )
    agent_specs = {AGENT_ID: agent_spec}
    agent_interfaces = {
        agent_id: agent.interface for agent_id, agent in agent_specs.items()
    }

    scenarios_iterator = Scenario.scenario_variations(
        scenarios, list(agent_specs.keys()),
    )

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
    # start service
    while True:
        print("new episode")
        import pdb

        pdb.set_trace()  # reset
        scenario = next(scenarios_iterator)
        observations = s.reset(scenario)

        import pdb

        pdb.set_trace()  # start running scenario
        step = 0
        while step < 100:
            agent_obs = observations.get(AGENT_ID)
            agent_action = agent.act(agent_obs)
            observations, _, _, _ = s.step({AGENT_ID: agent_action})
            step += 1

        import pdb

        pdb.set_trace()  # stop running scenario


if __name__ == "__main__":
    main(["scenarios/loop"])
