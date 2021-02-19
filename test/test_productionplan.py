import requests

from test.helpers import *
from test.fixtures import *

__PRODUCTION_PLAN_URI = "http://localhost:8888/productionplan/"

def test_windy_input(windy):
    r = requests.post(f"{__PRODUCTION_PLAN_URI}", json=windy)
    assert r.status_code == 200
    print(r.json())
    assert compute_load(r.json()) == windy["load"]

def test_no_wind_input(no_wind):
    r = requests.post(f"{__PRODUCTION_PLAN_URI}", json=no_wind)
    assert r.status_code == 200

def test_high_load(high_load):
    r = requests.post(f"{__PRODUCTION_PLAN_URI}", json=high_load)
    assert r.status_code == 200

def test_empty_payload():
    r = requests.post(f"{__PRODUCTION_PLAN_URI}", json={})
    assert r.status_code == 400

def test_None_payload():
    r = requests.post(f"{__PRODUCTION_PLAN_URI}", json=None)
    assert r.status_code == 400