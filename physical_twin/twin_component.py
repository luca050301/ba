from enum import Enum


class TwinComponent(Enum):
    """
    Enum representing different components in the digital twin system.
    """

    ROBOT = "my_robot"
    ENVIRONMENT = "my_env"
    PLANT = "my_plants"
    IRRIGATION = "irrigation"
