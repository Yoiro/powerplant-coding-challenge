import json
from pathlib import Path

import pytest

from app.planner import Planner
from app.schemas import Forecast


@pytest.fixture
def payload3():
    with open(Path(__file__).parent / "payloads" / "payload3.json") as f:
        return json.load(f)


@pytest.fixture
def planner(payload3):
    return Planner(forecast=Forecast(**payload3))


def test_add_cost_to_plants(planner):
    planner.add_cost_to_plants()
    expected_costs = {
        "gasfiredbig1": 13.4 / 0.53,
        "gasfiredbig2": 13.4 / 0.53,
        "gasfiredsomewhatsmaller": 13.4 / 0.37,
        "tj1": 50.8 / 0.3,
        "windpark1": 0,
        "windpark2": 0,
    }
    for plant in planner.plants:
        assert plant.cost == expected_costs[plant.name]


def test_sort_plants_by_cost(planner):
    planner.add_cost_to_plants()
    sorted_plants = planner.sort_plants_by_cost()
    expected_order = [
        "windpark1",
        "windpark2",
        "gasfiredbig1",
        "gasfiredbig2",
        "gasfiredsomewhatsmaller",
        "tj1",
    ]
    for i, plant in enumerate(sorted_plants):
        assert plant.name == expected_order[i]
