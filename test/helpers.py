__all__ = [
    "compute_load"
]

def compute_load(payload):
    load = 0
    for plant in payload:
        load += plant["p"]
    return load
