from pathlib import Path

from smarts.sstudio import types as t
from smarts.sstudio import gen_scenario


traffic = t.Traffic(
    flows=[
        t.Flow(
            route=t.Route(begin=("west", 0, 5), end=("east", 0, "max"),),
            rate=1,
            actors={t.TrafficActor("car"): 1},
        )
    ]
)

# stable_config = {
#     "theta": 9.3,
#     "position": 10,
#     "obstacle": 10,
#     "u_accel": 10,
#     "u_yaw_rate": 40,
#     "terminal": 0.05,
#     "impatience": 0,
#     "speed": 0.01,
# }


# aggressive_config = {
#     "theta": 1.3,
#     "position": 1.2,
#     "obstacle": 3,
#     "u_accel": 10,
#     "u_yaw_rate": 10,
#     "terminal": 0.05,
#     "impatience": 0,
#     "speed": 0.01,
# }

# aggressive_open_actor = t.SocialAgentActor(
#     name="open-agent-aggressive",
#     agent_locator="open_agent:open_agent-v0",
#     policy_kwargs={"gains": aggressive_config},
#     initial_speed=20,
# )


stable_open_actor = t.SocialAgentActor(
    name="open-agent-default",
    agent_locator="open_agent:open_agent-v0",
    initial_speed=20,
)

social_agent_missions = {
    "all": (
        [stable_open_actor],
        [
            t.Mission(
                t.Route(begin=("west", 1, 10), end=("east", 0, "max")), task=t.CutIn(),
            )
        ],
    ),
}

scenario = t.Scenario(
    traffic={"all": traffic}, social_agent_missions=social_agent_missions,
)

gen_scenario(scenario, output_dir=str(Path(__file__).parent))
