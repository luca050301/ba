from .sensor_interface import SensorInterface
from util.overrides_annotation import overrides
import simulation


class TemperatureSensor(SensorInterface):
    """
    This class represents a temperature sensor in the digital twin system.
    """

    @overrides(SensorInterface)
    def read_data(self):
        """
        Reads data from the temperature sensor.
        Returns:
            float: The current temperature in the simulation environment, measured in degrees Celsius.
        """
        return simulation.get_environment().temperature
