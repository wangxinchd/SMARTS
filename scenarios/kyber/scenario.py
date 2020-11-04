import random
from pathlib import Path

from smarts.sstudio import types as t
from smarts.sstudio import gen_scenario

# Specify agents
laner_agent = t.SocialAgentActor(
    name="keep-lane-agent", agent_locator="zoo.policies:keep-lane-agent-v0",
)

non_interactive_agent = t.SocialAgentActor(
    name=f"non-interactive-agent",
    agent_locator="zoo.policies:non-interactive-agent-v0",
    policy_kwargs={"speed": 10},
)

open_agent = t.SocialAgentActor(
    name="open-agent",
    agent_locator="zoo.policies.open-agent.open_agent:open_agent-v0"
)

social_agent_missions = {
    "agent-group-1": (
        [
            laner_agent,
            non_interactive_agent,
            open_agent
        ],
        [
            t.Mission(route=t.RandomRoute()),
        ]
    ),
    # "agent-group-2": (
    #     [
    #         laner_agent,
    #         non_interactive_agent,
    #         open_agent
    #     ],
    #     [
    #         t.Mission(route=t.RandomRoute()),
    #     ]
    # ),
}

gen_scenario(
    t.Scenario(
        social_agent_missions=social_agent_missions,
    ),
    output_dir=Path(__file__).parent,
)
