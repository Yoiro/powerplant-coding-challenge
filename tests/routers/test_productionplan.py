import json
import pytest

from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def payload1():
    with open("tests/payloads/payload1.json", "r") as f:
        return json.load(f)


@pytest.fixture
def payload2():
    with open("tests/payloads/payload2.json", "r") as f:
        return json.load(f)


@pytest.fixture
def payload3():
    with open("tests/payloads/payload3.json", "r") as f:
        return json.load(f)


@pytest.fixture
def response1():
    with open("tests/answers/response1.json", "r") as f:
        return json.load(f)


@pytest.fixture
def response2():
    with open("tests/answers/response2.json", "r") as f:
        return json.load(f)


@pytest.fixture
def response3():
    with open("tests/answers/response3.json", "r") as f:
        return json.load(f)


@pytest.fixture
def client():
    return TestClient(app)


def test_production_plan_payload1(client, payload1, response1):
    response = client.post("/productionplan", json=payload1)
    assert response.status_code == 200
    assert response.json() == response1
    assert sum(p["p"] for p in response.json()) == payload1["load"]


def test_production_plan_payload2(client, payload2, response2):
    response = client.post("/productionplan", json=payload2)
    assert response.status_code == 200
    assert response.json() == response2
    assert sum(p["p"] for p in response.json()) == payload2["load"]


def test_production_plan_payload3(client, payload3, response3):
    response = client.post("/productionplan", json=payload3)
    assert response.status_code == 200
    assert response.json() == response3
    assert sum(p["p"] for p in response.json()) == payload3["load"]


def test_production_plan_payload1_lp(client, payload1, response1):
    response = client.post("/productionplan", json=payload1, params={"solver": "lp"})
    assert response.status_code == 200
    assert response.json() == response1
    assert sum(p["p"] for p in response.json()) == payload1["load"]


def test_production_plan_payload2_lp(client, payload2, response2):
    response = client.post("/productionplan", json=payload2, params={"solver": "lp"})
    assert response.status_code == 200
    assert response.json() == response2
    assert sum(p["p"] for p in response.json()) == payload2["load"]


def test_production_plan_payload3_lp(client, payload3, response3):
    response = client.post("/productionplan", json=payload3, params={"solver": "lp"})
    assert response.status_code == 200
    assert response.json() == response3
    assert sum(p["p"] for p in response.json()) == payload3["load"]
