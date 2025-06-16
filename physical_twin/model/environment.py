class Environment:
    """
    A Class representing the parameters of the environment in which the digital twin operates.
    
    Attributes:
        temperature (float): The current temperature in degrees Celsius.
        humidity (float): The current humidity percentage.
        light (float): The current light intensity in arbitrary units.
    """

    def __init__(self, temperature=27.0, humidity=60.0, light=15000):
        self.temperature = temperature
        self.humidity = humidity
        self.light = light

    def update_environment(self, temperature=None, humidity=None, light=None):
        if temperature is not None:
            self.temperature = temperature
        if humidity is not None:
            self.humidity = humidity
        if light is not None:
            self.light = light