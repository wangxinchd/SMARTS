import pytest
import shutil
import tempfile

from pathlib import Path
from unittest.mock import MagicMock
from smarts.core.scenario import Scenario
from smarts.core.traffic_history_provider import TrafficHistoryProvider
from smarts.sstudio.sumo2mesh import generate_glb_from_sumo_network
from smarts.sstudio import gen_social_agent_missions, gen_missions
from smarts.sstudio.types import Mission, Route, SocialAgentActor

AGENT_ID = "Agent-007"


@pytest.fixture
def scenario_parent_path():
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def create_scenario(scenario_parent_path):
    scenario = Path(scenario_parent_path) / "cycles"
    scenario.mkdir()

    shutil.copyfile(
        Path(__file__).parent / "maps/6lane.net.xml", scenario / "map.net.xml"
    )
    generate_glb_from_sumo_network(
        str(scenario / "map.net.xml"), str(scenario / "map.glb")
    )

    actors = [
        SocialAgentActor(
            name=f"non-interactive-agent-{speed}-v0",
            agent_locator="zoo.policies:non-interactive-agent-v0",
            policy_kwargs={"speed": speed},
        )
        for speed in [10, 30]
    ]

    for name, (edge_start, edge_end) in [
        ("group-1", ("edge-north-NS", "edge-south-NS")),
        ("group-2", ("edge-west-WE", "edge-east-WE")),
        ("group-3", ("edge-east-EW", "edge-west-EW")),
        ("group-4", ("edge-south-SN", "edge-north-SN")),
    ]:
        route = Route(begin=("edge-north-NS", 1, 0), end=("edge-south-NS", 1, "max"))
        missions = [Mission(route=route)] * 2
        gen_social_agent_missions(
            scenario, social_agent_actor=actors, name=name, missions=missions,
        )

    return scenario


def test_mutiple_traffic_data(create_scenario):
    Scenario.discover_traffic_histories = MagicMock(
        return_value=[{"1": "history"}, {"2": "history2"}]
    )
    iterator = Scenario.variations_for_all_scenario_roots(
        [str(create_scenario)], [AGENT_ID]
    )
    scenarios = list(iterator)

    assert len(scenarios) == 8  # 2 social agents x 2 missions x 2 histories

    traffic_history_provider = TrafficHistoryProvider()

    for scenario in scenarios:
        assert scenario.traffic_history  # all scenarios have history

        traffic_history_provider.setup(scenario)
        assert traffic_history_provider._current_traffic_history
