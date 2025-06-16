from .sensor_interface import SensorInterface
from util.overrides_annotation import overrides
import simulation


class LightSensor(SensorInterface):
    """
    This class represents a light sensor in the digital twin system.
    """

    @overrides(SensorInterface)
    def read_data(self):
        """
        Reads data from the light sensor.
        Returns:
            float: The current light intensity in the simulation environment, measured in lux.
        """
        return simulation.get_environment().light
