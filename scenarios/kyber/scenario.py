import pickle
import random
import os
from pathlib import Path

from smarts.sstudio import types as t
from smarts.sstudio import gen_scenario


with open(os.environ["SOCIAL_AGENT_PATH"], "rb") as f:
    social_agents = pickle.load(f)


social_agent_missions = {
    "agent-group-1": (social_agents, [t.Mission(route=t.RandomRoute()),]),
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
    t.Scenario(social_agent_missions=social_agent_missions,),
    output_dir=Path(__file__).parent,
)
