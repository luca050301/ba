from datetime import datetime
import random
from datetime import timedelta

class Plant:
    """
    A class representing a plant in the digital twin system.
    Attributes:
        id (int): Unique identifier for the plant.
        has_plant (bool): Indicates if a plant is planted in the pot.
        base_water_consumption (float): Base water consumption rate of the plant per day.
        base_nutrient_consumption (float): Base nutrient consumption rate of the plant per day.
        datetime_planted (datetime): Timestamp when the plant was planted.
        moisture_level (float): Current moisture level of the plant's soil.
        nutrient_level (float): Current nutrient level of the plant's soil.
        healthy (bool): Indicates if the plant is healthy.
        i
    """

    MIN_MOISTURE = 0.3
    MIN_NUTRIENTS = 0.3

    MAX_MOISTURE = 1.0
    MAX_NUTRIENTS = 1.0
    
    moisture_level: float = 1.0
    nutrient_level: float = 1.0
    healthy: bool = True
    
    datetime_planted: datetime

    def __init__(self, id: int, has_plant: bool = True, base_water_consumption: float = 0.03, base_nutrient_consumption: float = 0.03, date_time_planted: datetime = None):
        self.id = id
        self.has_plant = has_plant
        self.base_water_consumption = base_water_consumption
        self.base_nutrient_consumption = base_nutrient_consumption
        
        if date_time_planted is not None:
            self.datetime_planted = date_time_planted
        else:
            self.set_random_datetime_planted()
        
    def set_random_datetime_planted(self):
        """
        Sets a random datetime for when the plant was planted, within the last 16 weeks.
        """
        now = datetime.now()
        sixteen_weeks_ago = now - timedelta(weeks=16)
        random_seconds = random.randint(0, int((now - sixteen_weeks_ago).total_seconds()))
        self.datetime_planted = sixteen_weeks_ago + timedelta(seconds=random_seconds)

    def is_harvestable(self) -> bool:
        """
        Checks if the plant is harvestable based on its age.
        
        Returns:
            bool: True if the plant is harvestable, False otherwise.
        """
        return self.has_plant and self.datetime_planted is not None and (datetime.now() - self.datetime_planted).days >= 15 * 7
    
    def is_plantable(self) -> bool:
        """
        Checks if the plant is planted in the pot.
        
        Returns:
            bool: True if the pot is empty (no plant), False otherwise.
        """
        return not self.has_plant

    def should_water(self) -> bool:
        """
        Checks if the plant needs watering.
        
        Returns:
            bool: True if the plant needs watering, False otherwise.
        """
        return self.has_plant and self.moisture_level < self.MIN_MOISTURE
    
    def should_fertilize(self) -> bool:
        """
        Checks if the plant needs fertilization.
        
        Returns:
            bool: True if the plant needs fertilization, False otherwise.
        """
        return self.has_plant and self.nutrient_level < self.MIN_NUTRIENTS