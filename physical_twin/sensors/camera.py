from .sensor_interface import SensorInterface
from util.overrides_annotation import overrides


class Camera(SensorInterface):
    """
    This class represents a camera sensor in the digital twin system.
    """

    @overrides(SensorInterface)
    def read_data(self):
        """
        Reads data from the camera sensor.
        Returns:
            str: A placeholder string representing the image data captured by the camera.
        """
        return "image_data_placeholder"
