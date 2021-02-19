import requests

from test.helpers import *
from test.fixtures import *

__PRODUCTION_PLAN_URI = "http://127.0.0.1:8888/productionplan/"

def test_windy_input(windy):
    r = requests.post(f"{__PRODUCTION_PLAN_URI}", json=windy)
    assert r.status_code == 200
    assert compute_load(r.json()) == windy["load"]

def test_no_wind_input(no_wind):
    r = requests.post(f"{__PRODUCTION_PLAN_URI}", json=no_wind)
    assert r.status_code == 200
    assert compute_load(r.json()) == no_wind["load"]

def test_high_load(high_load):
    r = requests.post(f"{__PRODUCTION_PLAN_URI}", json=high_load)
    assert r.status_code == 200
    assert compute_load(r.json()) == high_load["load"]

def test_empty_payload():
    r = requests.post(f"{__PRODUCTION_PLAN_URI}", json={})
    assert r.status_code == 400

def test_none_payload():
    r = requests.post(f"{__PRODUCTION_PLAN_URI}", json=None)
    assert r.status_code == 400

def test_missing_keys():
    r = requests.post(f"{__PRODUCTION_PLAN_URI}", json={"load": 0})
    assert r.status_code == 500

def test_all_load(all_load):
    r = requests.post(f"{__PRODUCTION_PLAN_URI}", json=all_load)
    assert r.status_code == 202