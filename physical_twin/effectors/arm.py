import sys
import os
import random
from model.plant import Plant


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from sensors.sensor_interface import SensorInterface
from util.overrides_annotation import overrides


class Arm(SensorInterface):
    """A class representing the arm of the roboter

    Attributes:
        position (list): The current position of the arm in 3D space, represented as [x, y, z].
    """

    def __init__(self, position=[0.0, 0.0, 0.0]):
        self.position = position

    @overrides(SensorInterface)
    def read_data(self):
        """
        Reads data from the arm sensor.
        Returns:
            list: The current position of the arm in 3D space, represented as [x, y, z].
        """
        # Placeholder for actual arm data reading logic
        # In a real implementation, this would interface with the arm's hardware or software API
        return self.position

    def position_at_plant(self, plant: Plant):
        """
        Moves the arm to the position of the specified plant.
        In the current implementation, it randomly generates a position.

        Parameters:
            plant (Plant): The plant object for which the arm's position is to be determined.
        """
        plant_position = [
            random.uniform(-0.2, 0.2),
            (-1 if plant.id % 2 == 0 else 1) * random.uniform(0.5, 1.5),
            random.uniform(0, 0.8),
        ]
