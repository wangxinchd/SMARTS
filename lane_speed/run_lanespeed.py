import argparse
from pathlib import Path

import gym

from smarts.core.agent import AgentPolicy
from smarts.core.agent import AgentSpec
from smarts.core.agent_interface import AgentInterface, AgentType
from smarts.core.controllers import ActionSpaceType

target_speed = 3


class LanespeedPolicy(AgentPolicy):
    def act(self, obs):
        global target_speed
        print(
            f"command speed: {target_speed}, actual speed: {obs.ego_vehicle_state.speed}"
        )
        return (target_speed, 0)


def parse_args():
    parser = argparse.ArgumentParser("run simple keep lane agent")
    # env setting
    parser.add_argument("scenario", type=str, help="Path to scenario")
    parser.add_argument(
        "--headless", default=False, action="store_true", help="Turn on headless mode"
    )

    return parser.parse_args()


def main(args):
    scenario_path = Path(args.scenario).absolute()

    AGENT_ID = "AGENT-007"

    agent_interface = AgentInterface.from_type(AgentType.LanerWithSpeed)
    agent_interface.max_episode_steps = 150

    agent_spec = AgentSpec(
        interface=agent_interface, policy_builder=lambda: LanespeedPolicy()
    )

    env = gym.make(
        "smarts.env:hiway-v0",
        scenarios=[scenario_path],
        agent_specs={AGENT_ID: agent_spec},
        # set headless to false if u want to use envision
        headless=False,
        visdom=False,
        seed=42,
    )

    agent = agent_spec.build_agent()

    while True:
        global target_speed
        observations = env.reset()
        total_reward = 0.0
        dones = {"__all__": False}

        while not dones["__all__"]:
            agent_obs = observations[AGENT_ID]
            agent_action = agent.act(agent_obs)
            observations, rewards, dones, _ = env.step({AGENT_ID: agent_action})
            total_reward += rewards[AGENT_ID]

        print("*" * 100)
        print("Accumulated reward:", total_reward)
        target_speed += 1

    env.close()


if __name__ == "__main__":
    args = parse_args()
    main(args)
