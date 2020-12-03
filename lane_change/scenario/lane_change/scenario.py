from pathlib import Path

from smarts.sstudio import gen_missions
from smarts.sstudio.types import (
    Route,
    Mission,
)


scenario = str(Path(__file__).parent)


gen_missions(
    scenario=scenario,
    missions=[Mission(Route(begin=("gneE6", 1, 20), end=("gneE6", 0, "max"))),],
    overwrite=True,
)
