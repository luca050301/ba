"""
Simulation module for the Digital Twin project.
Used to simulate the environment and plant growth dynamics.
"""

from model.environment import Environment
from model.plant import Plant
import time
import random
import effectors.irrigation as irrigation

_environment = None
_plants = None
_initialized = False
_cycle_time : int


def initialize(environment: Environment, plants: list[Plant], cycle_time: int = 10):
    """
    Initializes the simulation module with the given environment and plants.
    This function should be called once before using other functions.
    """
    global _environment, _plants, _initialized, _cycle_time
    _environment = environment
    _plants = plants
    _initialized = True
    _cycle_time = cycle_time
    


def get_environment():
    """
    Returns the environment of the simulation.
    """
    return _environment


def get_plants():
    """
    Returns the list of plants in the simulation.
    """
    return _plants


def run_cycle():
    """
    Runs a simulation cycle - updates the environment and plant states.
    """
    print("running cycle")
    
    _environment.temperature += random.uniform(-0.5, 0.5)
    _environment.humidity += random.uniform(-0.5, 0.5)
    _environment.light += random.randint(-100, 100)
    
    for plant in _plants:
        # update the plant's moisture and nutrient levels based on irrigation/fertigation and consumption
        plant.moisture_level = min(
            max(
                plant.moisture_level
                + irrigation.read_data()
                - plant.base_water_consumption * random.uniform(0.8, 1.2),
                0.0,
            ),
            1.0,
        )
        plant.nutrient_level = min(
            max(
                plant.nutrient_level
                + irrigation.read_data()
                - plant.base_nutrient_consumption * random.uniform(0.8, 1.2),
                0.0,
            ),
            1.0,
        )
        # small chance of the plant getting sick, increased by suboptimal moisture or nutrient levels
        if plant.healthy:
            sickness_chance = (
                0.005
                if plant.moisture_level >= Plant.MIN_MOISTURE
                and plant.nutrient_level >= Plant.MIN_NUTRIENTS
                else 0.02
            )
            plant.healthy = random.random() > sickness_chance


def run_simulation():
    while True:
        run_cycle()
        time.sleep(_cycle_time)
