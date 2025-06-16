from .sensor_interface import SensorInterface
from util.overrides_annotation import overrides
import simulation


class SoilNutrientSensor(SensorInterface):
    """
    This class represents a soil nutrient sensor in the digital twin system.
    """

    @overrides(SensorInterface)
    def read_data_at_plant(self, id):
        """
        Reads data from the soil nutrient sensor.
        Parameters:
            id (int): The ID of the plant where the soil nutrient data is to be read.
        Returns:
            float: The current soil nutrient level at the specified plant location, measured in percent of nutrient saturation.
        """
        return simulation.get_plants()[id].nutrient_level
