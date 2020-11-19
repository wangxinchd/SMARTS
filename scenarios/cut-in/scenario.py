import os
from pathlib import Path

from smarts.sstudio import gen_scenario
from smarts.sstudio import types as t


traffic = t.Traffic(
    flows=[
        t.Flow(
            route=t.Route(begin=("edge-west-WE", 0, 0), end=("edge-east-WE", 0, "max")),
            rate=1,
            actors={t.TrafficActor(name="car", depart_speed=5): 1.0},
        )
    ]
)

social_agent_missions = {
    "open": (
        [
            t.SocialAgentActor(
                name="open-agent",
                agent_locator="open_agent:open_agent-v0",
                initial_speed=10,
            ),
        ],
        [
            t.Mission(
                t.Route(begin=("edge-west-WE", 1, 20), end=("edge-west-WE", 0, "max")),
                task=t.CutIn(),
            )
        ],
    ),
}

ego_missions = [
    t.Mission(
        t.Route(begin=("edge-west-WE", 1, 20), end=("edge-east-WE", 0, "max")),
        task=t.CutIn(),
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
