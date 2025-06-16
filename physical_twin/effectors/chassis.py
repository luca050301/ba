import sys
import os
from model.plant import Plant

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from sensors.sensor_interface import SensorInterface
from util.overrides_annotation import overrides


class Chassis(SensorInterface):
    """
    This class represents a chassis in the digital twin system.
    """

    def __init__(self, position=0, plant_count=5):
        """
        Initializes the chassis with a given position and the number of plants it can interact with.

        Parameters:
            position (int): The initial position of the chassis.
            plant_count (int): The number of plants the chassis can interact with.
        """
        self.position = position
        self.plant_count = plant_count  # Number of plants the chassis can interact with

    @overrides(SensorInterface)
    def read_data(self):
        """
        Reads data from the chassis sensor.
        Returns:
            int: The current position of the chassis.
        """
        return self.position

    def move_to(self, plant: Plant):
        """
        Moves the chassis to the position of the specified plant.
        Parameters:
            plant (Plant): The plant object for which the chassis's position is to be set.
        """
        self.position = plant.id

    def move_to_next(self):
        """
        Moves the chassis to the next position.
        This method cycles through the positions based on the number of plants.
        """
        self.position = (self.position + 1) % self.plant_count
