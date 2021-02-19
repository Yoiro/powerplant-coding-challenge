import json
import os
from pathlib import Path

import requests
import pytest

__PRODUCTION_PLAN_URI = "http://localhost:5000/productionplan/"
__TEST_DIR = Path(__file__).parents[0]

@pytest.fixture
def windy():
    payload = __TEST_DIR / "mocks" / "payload1.json"
    return json.load(open(payload))

@pytest.fixture
def no_wind():
    payload = __TEST_DIR / "mocks" / "payload2.json"
    return json.load(open(payload))

@pytest.fixture
def high_load():
    payload = __TEST_DIR / "mocks" / "payload3.json"
    return json.load(open(payload))

def compute_load(payload):
    load = 0
    for plant in payload:
        load += plant["p"]
    return load

def test_windy_input(windy):
    r = requests.post(f"{__PRODUCTION_PLAN_URI}", json=windy)
    assert r.status_code == 200
    assert compute_load(r.json()) == windy["load"]

def test_no_wind_input(no_wind):
    r = requests.post(f"{__PRODUCTION_PLAN_URI}", json=no_wind)
    assert r.status_code == 200

def test_high_load(high_load):
    r = requests.post(f"{__PRODUCTION_PLAN_URI}", json=high_load)
    assert r.status_code == 200
