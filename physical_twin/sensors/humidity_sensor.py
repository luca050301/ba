from .sensor_interface import SensorInterface
from util.overrides_annotation import overrides
import simulation


class HumiditySensor(SensorInterface):
    """
    This class represents a humidity sensor in the digital twin system.
    """

    @overrides(SensorInterface)
    def read_data(self):
        """
        Reads data from the humidity sensor.
        Returns:
            float: The current humidity level in the simulation environment.
        """
        return simulation.get_environment().humidity
