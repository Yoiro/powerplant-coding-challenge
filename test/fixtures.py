import json
from pathlib import Path

import pytest

__all__ = [
    "windy",
    "no_wind",
    "high_load",
    "all_load",
    "no_load",
    "negative_load",
]

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

@pytest.fixture
def all_load():
    payload = __TEST_DIR / "mocks" / "payload4.json"
    return json.load(open(payload))

@pytest.fixture
def no_load():
    payload = __TEST_DIR / "mocks" / "payload5.json"
    return json.load(open(payload))

@pytest.fixture
def negative_load():
    payload = __TEST_DIR / "mocks" / "payload6.json"
    return json.load(open(payload))