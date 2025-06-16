from enum import Enum


class RobotState(Enum):
    """
    Enum representing the state of a robot.
    """

    IDLE = "idle"
    SEEDING = "seeding"
    WATERING = "watering"
    FERTILIZING = "fertilizing"
    HARVESTING = "harvesting"
    MONITORING = "monitoring"
    AUTO = "auto"
