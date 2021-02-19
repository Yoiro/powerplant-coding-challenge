import json
import re

from flask import current_app

_lookup = {
    "gasfired": "gas",
    "turbojet": "kerosine",
    "windturbine": "wind"
}


class PowerPlant:
    def __init__(self, name=None, type=None, efficiency=0.0, pmin=0, pmax=0):
        self.name = name
        self.type = type
        self.efficiency = efficiency
        self.pmin = pmin
        self.pmax = pmax
        self.produced_power = 0

    def __str__(self):
        return f"{self.name}: {self.type}"

    def __repr__(self):
        return f"{self.name}"


class Fuel:
    def __init__(self, name, unit, price):
        self.name = name
        self.unit = unit
        self.price = price


class Network:
    def __init__(self, load=0, fuels=None, powerplants=None):
        self.load = load
        self.fuels = {} if fuels is None else fuels
        self.powerplants = [] if powerplants is None else powerplants
        self.activated_plants = []

    def remove_wind_from_plants(self, plants):
        return list(filter(
            lambda p: p.type != "windturbine", plants
        ))

    def define_merit_order(self):
        plants = self.powerplants
        order = []
        if self.fuels["wind"].price == 0:
            plants = self.remove_wind_from_plants(plants)
        for plant in plants:
            order.append((self.powerplants.index(plant), (self.fuels[_lookup[plant.type]].price * (1 - plant.efficiency))))
        order.sort(key=lambda p: p[1])
        return order

    def compute_production_plan(self):
        load = 0
        plant_count = 0
        while load != self.load:
            merit_order = self.define_merit_order()
            current_app.logger.debug(merit_order)
            current_plant = self.powerplants[merit_order[plant_count][0]]
            multiplicator = 1
            if current_plant.type == "windturbine":
                multiplicator = self.fuels["wind"].price / 100
            produced_power = (current_plant.pmax - current_plant.pmin) * multiplicator
            new_load = produced_power + load
            if new_load > self.load:
                # if the power outweights the target load
                # we remove the difference between the "new" load that will
                # be reached by adding that produced_power
                # and the target load.
                produced_power -= new_load - self.load
                if produced_power < current_plant.pmin:
                    plant_count += 1
                    continue
            current_plant.produced_power = round(produced_power, 1)
            load += current_plant.produced_power
            # Increment the counter in order to get the next plant
            plant_count += 1
            current_app.logger.debug(f"load {plant_count} = {load}")
            current_app.logger.debug(f"target load = {self.load} => {self.load == load}")
            self.activated_plants.append(current_plant)

    def create_response(self):
        response = []
        for plant in self.powerplants:
            response.append({"name": plant.name, "p": plant.produced_power})
        return response

    @staticmethod
    def load_network_from_json(payload):
        network = Network()

        network.load = payload["load"]

        fuels = payload["fuels"]
        for key, val in fuels.items():
            name = key.split("(")[0]
            unit = re.search(r".*\((.*)\)", key).group(1)
            price = val
            network.fuels[name] = Fuel(name, unit, price)

        for plant in payload["powerplants"]:
            network.powerplants.append(PowerPlant(**plant))

        return network
