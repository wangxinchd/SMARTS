import os
from pathlib import Path

from smarts.sstudio import gen_scenario
from smarts.sstudio import types as t


traffic = t.Traffic(
    flows=[
        t.Flow(
            route=t.Route(begin=("edge-west-EW", 0, 0), end=("edge-west-EW", 0, "max")),
            rate=1,
            actors={t.TrafficActor(name="car"): 1.0},
            begin=6,
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


social_agent_missions = {
    "all": (
        [
            # t.SocialAgentActor(
            #     name="open-agent-default", agent_locator="open_agent:open_agent-v0"
            # ),
            t.SocialAgentActor(
                name="open-agent-aggressive",
                agent_locator="open_agent:open_agent-v0",
                policy_kwargs={"gains": aggressive_config}
            ),
            t.SocialAgentActor(
                name="open-agent-stable",
                agent_locator="open_agent:open_agent-v0",
                policy_kwargs={"gains": stable_config}
            ),
        ],
        [
            t.Mission(
                t.Route(begin=("edge-west-WE", 0, 30), end=("edge-west-EW", 0, "max")),
                task=t.UTurn(target_lane_index=0),
            )
        ],
    ),
}

ego_missions = [
    t.Mission(
        t.Route(begin=("edge-west-WE", 0, 50), end=("edge-west-EW", 0, "max")),
        task=t.UTurn(),
    )
]

gen_scenario(
    scenario=t.Scenario(
        traffic={"basic": traffic},
        # ego_missions=ego_missions,
        social_agent_missions=social_agent_missions,
    ),
    output_dir=Path(__file__).parent,
)