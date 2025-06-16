from .sensor_interface import SensorInterface
from util.overrides_annotation import overrides
import simulation


class SoilMoistureSensor(SensorInterface):
    """
    This class represents a soil moisture sensor in the digital twin system.
    """

    @overrides(SensorInterface)
    def read_data_at_plant(self, id):
        """
        Reads data from the soil moisture sensor.
        Parameters:
            id (int): The ID of the plant where the soil moisture data is to be read.
        Returns:
            float: The current soil moisture level at the specified plant location.
        """
        return simulation.get_plants()[id].moisture_level
