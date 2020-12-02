import os
from pathlib import Path

from smarts.sstudio import gen_scenario
from smarts.sstudio import types as t


traffic = t.Traffic(
    flows=[
        t.Flow(
            route=t.Route(
                begin=("edge-west-WE", 0, 10), end=("edge-west-WE", 0, "max")
            ),
            rate=1,
            actors={t.TrafficActor(name="car"): 1.0},
            # begin=0,
        )
    ]
)

stable_config = {
    "theta": 9.3,
    "position": 10,
    "obstacle": 10,
    "u_accel": 10,
    "u_yaw_rate": 40,
    "terminal": 0.05,
    "impatience": 0,
    "speed": 0.01,
}


aggressive_config = {
    "theta": 1.3,
    "position": 1.2,
    "obstacle": 3,
    "u_accel": 10,
    "u_yaw_rate": 10,
    "terminal": 0.05,
    "impatience": 0,
    "speed": 0.01,
}

npc_actor = t.SocialAgentActor(
    name=f"npc-agent",
    agent_locator="zoo.policies:non-interactive-agent-v0",
    policy_kwargs={"speed": 20},
)


aggressive_open_actor = t.SocialAgentActor(
    name="open-agent-aggressive",
    agent_locator="open_agent:open_agent-v0",
    policy_kwargs={"gains": aggressive_config},
)


stable_open_actor = t.SocialAgentActor(
    name="open-agent-stable",
    agent_locator="open_agent:open_agent-v0",
    policy_kwargs={"gains": stable_config},
)

social_agent_missions = {
    "all": (
        [npc_actor],
        [
            t.Mission(
                t.Route(begin=("edge-west-EW", 0, 0), end=("edge-west-EW", 0, "max")),
            )
        ],
    )
}

# ego_missions = [
#     t.Mission(
#         t.Route(begin=("edge-west-WE", 0, 50), end=("edge-west-EW", 0, "max")),
#         task=t.UTurn(),
#     )
# ]

gen_scenario(
    scenario=t.Scenario(
        traffic={"basic": traffic},
        # ego_missions=ego_missions,
        social_agent_missions=social_agent_missions,
        bubbles=[
            t.Bubble(
                zone=t.PositionalZone(pos=(50, 0), size=(10, 15)),
                margin=5,
                actor=stable_open_actor,
                follow_actor_id=t.Bubble.to_actor_id(npc_actor, mission_group="all"),
                follow_offset=(-7, 10),
            ),
        ],
    ),
    output_dir=Path(__file__).parent,
)
