class SensorInterface:
    """
    This class serves as an interface for sensor data handling.
    It provides methods to read sensor data.
    """

    def read_data(self):
        """
        Reads data from the sensor.
        Returns:
            The sensor data.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    def read_data_at_plant(self, plant_id):
        """
        Reads data from the sensor at a specific plant location.
        Parameters:
            plant_id (int): The ID of the plant where the sensor data is to be read.
        Returns:
            The sensor data at the specified plant location.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")
