import time
from effectors.chassis import Chassis
from effectors.arm import Arm
from sensors.camera import Camera
from sensors.humidity_sensor import HumiditySensor
from sensors.soil_moisture_sensor import SoilMoistureSensor
from sensors.temperature_sensor import TemperatureSensor
from sensors.light_sensor import LightSensor
from sensors.soil_moisture_sensor import SoilMoistureSensor
from sensors.soil_nutrient_sensor import SoilNutrientSensor
from robot_state import RobotState
from model.plant import Plant
from twin_component import TwinComponent
import effectors.irrigation as irrigation
import logging
from datetime import datetime


class Robot:
    """
    A class representing a robot that manages plants in a greenhouse environment.
    The robot can perform various actions such as seeding, watering, fertilizing, harvesting,
    and monitoring plants. It is equipped with sensors and effectors to interact with the environment.
    Attributes:
        chassis (Chassis): The chassis of the robot, responsible for movement.
        arm (Arm): The robotic arm for performing tasks like seeding and harvesting.
        camera (Camera): The camera for monitoring the environment.
        humidity_sensor (HumiditySensor): Sensor for measuring humidity.
        temperature_sensor (TemperatureSensor): Sensor for measuring temperature.
        light_sensor (LightSensor): Sensor for measuring light levels.
        soil_moisture_sensor (SoilMoistureSensor): Sensor for measuring soil moisture.
        soil_nutrient_sensor (SoilNutrientSensor): Sensor for measuring soil nutrient levels.
        plants (list[Plant]): List of plants that the robot manages.
        position (int): The current position of the robot in the greenhouse.
        state (RobotState): The current state of the robot, indicating what action it is performing.
        measurement_queue (Queue): A queue for sending measurements via MQTT.
        cycle_time (int): The time interval for the robot's actions.
    """

    state = RobotState.IDLE
    plants: list[Plant] = []

    def __init__(
        self,
        plants,
        measurement_queue,
        action_queue,
        position=0,
        cycle_time: int = 10,  # Time interval for the robot's actions
    ):
        self.chassis = Chassis(plant_count=len(plants), position=position)
        self.arm = Arm()
        self.camera = Camera()
        self.humidity_sensor = HumiditySensor()
        self.temperature_sensor = TemperatureSensor()
        self.light_sensor = LightSensor()
        self.soil_moisture_sensor = SoilMoistureSensor()
        self.soil_nutrient_sensor = SoilNutrientSensor()
        self.plants = plants
        self.position = position  # Initial position of the robot
        self.cycle_time = cycle_time  # Time interval for the robot's actions
        self.measurement_queue = (
            measurement_queue  # Queue for measurements (to be sent via MQTT)
        )
        self.action_queue = (
            action_queue  # Queue for actions (to be processed by the robot)
        )
        self.logger = logging.getLogger(__name__)

    def set_state(self, state: RobotState):
        """
        Sets the state of the robot and sends the updated state via MQTT.
        Parameters:
            state (RobotState): The new state of the robot.
        """
        self.state = state
        self.send_mqtt_msg(
            TwinComponent.ROBOT, self.get_robot_data()
        )  # Send robot data via MQTT
        self.logger.info(f"Robot state changed to: {self.state.value}")

    def handle_state(self):
        """
        Handles the current state of the robot and performs the corresponding action.
        Sends the robot's data via MQTT after performing the action.
        Moves the robot to the next plant after each action.
        """
        if self.state == RobotState.IDLE:
            self.do_idle()
        elif self.state == RobotState.SEEDING:
            self.do_seeding()
        elif self.state == RobotState.WATERING:
            self.do_watering()
        elif self.state == RobotState.FERTILIZING:
            self.do_fertilizing()
        elif self.state == RobotState.HARVESTING:
            self.do_harvesting()
        elif self.state == RobotState.MONITORING:
            self.do_monitoring()
        elif self.state == RobotState.AUTO:
            self.do_auto()
        else:
            raise ValueError(f"Unknown state: {self.state}")

        if self.state is not RobotState.IDLE:
            self.move_to_next()  # Move to the next plant

    def do_idle(self):
        self.logger.info("Robot is idle.")
        # Do nothing.

    def do_seeding(self, send_mqtt_msg=True):
        """
        Checks if there already is a plant in the current position.
        If not, seeds a new plant in the current position.
        """
        self.logger.info("Robot is seeding.")

        plant = self.plants[self.chassis.position]

        if not plant.has_plant:
            self.seed_plant(plant, send_mqtt_msg=send_mqtt_msg)

    def do_watering(self, send_mqtt_msg=True):
        self.logger.info("Robot is watering.")

        plant = self.plants[self.chassis.position]
        self.water_plant(plant, send_mqtt_msg=send_mqtt_msg)

    def do_fertilizing(self, send_mqtt_msg=True):
        self.logger.info("Robot is fertilizing.")

        plant = self.plants[self.chassis.position]

        self.fertilize_plant(plant, send_mqtt_msg=send_mqtt_msg)

    def do_harvesting(self, send_mqtt_msg=True):
        """
        Checks if the plant in the current position is harvestable.
        If it is, harvests the plant.
        """
        self.logger.info("Robot is harvesting.")

        plant = self.plants[self.chassis.position]

        if plant.is_harvestable():
            self.harvest_plant(plant, send_mqtt_msg=send_mqtt_msg)

    def do_monitoring(self):
        """
        Send environmental data and plant data for the current position.
        """
        self.logger.info("Robot is monitoring.")

        self.send_mqtt_msg(TwinComponent.ENVIRONMENT, self.get_environmental_data())

        self.monitor_plant(self.chassis.position)

    def do_auto(self):
        """
        Performs all actions in autonomous mode: seeding, watering, fertilizing, harvesting, and monitoring.
        """
        self.logger.info("Robot is in autonomous mode.")

        self.do_seeding(send_mqtt_msg=False)
        self.do_watering(send_mqtt_msg=False)
        self.do_fertilizing(send_mqtt_msg=False)
        self.do_harvesting(send_mqtt_msg=False)
        self.do_monitoring()

    def get_temperature_data(self):
        return self.temperature_sensor.read_data()

    def get_humidity_data(self):
        return self.humidity_sensor.read_data()

    def get_light_data(self):
        return self.light_sensor.read_data()

    def get_soil_moisture_data(self, plant_id):
        return self.soil_moisture_sensor.read_data_at_plant(plant_id)

    def get_soil_nutrient_data(self, plant_id):
        return self.soil_nutrient_sensor.read_data_at_plant(plant_id)

    def get_plant_health_data(self, plant: Plant):
        return "healthy" if plant.healthy else "sick"

    def get_plant_ripeness_data(self, plant: Plant):
        return "ripe" if plant.is_harvestable() else "not ripe"

    def get_environmental_data(self):
        return {
            "temperature": self.get_temperature_data(),
            "humidity": self.get_humidity_data(),
            "light": self.get_light_data(),
        }

    def get_plant_data(self, plant_id):
        return {
            "soil_moisture": self.get_soil_moisture_data(plant_id) * 100,
            "soil_nutrients": self.get_soil_nutrient_data(plant_id) * 100,
            "health": self.get_plant_health_data(self.plants[plant_id]),
            "ripeness": self.get_plant_ripeness_data(self.plants[plant_id]),
            "datetime_planted": str(self.plants[plant_id].datetime_planted),
        }

    def get_robot_data(self):
        return {
            "position": self.chassis.position + 1,
            "arm_position": str(self.arm.position),
            "state": self.state.value,
        }

    def monitor_plant(self, plant_id):
        """
        Moves to the specified plant's position and sends its data via MQTT.
        Also sends the current irrigation flow rate.
        """

        self.move_to(plant_id)
        self.set_arm_position(self.plants[plant_id])
        self.send_mqtt_msg(
            TwinComponent.PLANT, self.get_plant_data(plant_id), plant_id + 1
        )
        self.send_mqtt_msg(
            TwinComponent.ROBOT,
            {
                "action": "monitor",
            },
        )
        self.send_mqtt_msg(
            TwinComponent.IRRIGATION, {"flow_rate": irrigation.read_data() * 100}
        )

    def seed_plant(self, plant: Plant, send_mqtt_msg=True):
        """
        Moves to the plant's position and positions the arm to seed the plant.
        Creates a new Plant instance and adds it to the plants list at the specified position.
        Sends a message via MQTT with the datetime when the plant was seeded.
        """
        if not plant.is_plantable():
            return
        self.logger.info(f"Seeding plant with ID: {plant.id}")

        self.move_to(plant.id, send_mqtt_msg=send_mqtt_msg)
        self.set_arm_position(plant, send_mqtt_msg=send_mqtt_msg)
        self.plants[plant.id] = Plant(
            id=plant.id, date_time_planted=datetime.now()
        )  # Create a seedling plant

        self.send_mqtt_msg(
            TwinComponent.ROBOT,
            {
                "action": "seed",
            },
        )

        if send_mqtt_msg:
            self.send_mqtt_msg(
                TwinComponent.PLANT,
                {"datetime_planted": str(self.plants[plant.id].datetime_planted)},
                plant.id + 1,
            )

    def harvest_plant(self, plant: Plant, send_mqtt_msg=True):
        """
        Moves to the plant's position and positions the arm to harvest the plant.
        Removes the plant from the pot by setting its has_plant attribute to False.
        Sends a message via MQTT that the plant pot is now empty (i.e., datetime_planted is None).
        """
        if not plant.is_harvestable():
            return

        self.logger.info(f"Harvesting plant with ID: {plant.id}")

        self.move_to(plant.id, send_mqtt_msg=send_mqtt_msg)
        self.set_arm_position(plant, send_mqtt_msg=send_mqtt_msg)
        self.plants[plant.id].has_plant = False  # Remove the plant from the pot
        self.plants[plant.id].datetime_planted = None  # Set datetime_planted to None

        self.send_mqtt_msg(
            TwinComponent.ROBOT,
            {
                "action": "harvest",
            },
        )

        if send_mqtt_msg:
            self.send_mqtt_msg(
                TwinComponent.PLANT,
                {"datetime_planted": str(plant.datetime_planted)},
                plant.id + 1,
            )

    def water_plant(self, plant: Plant, send_mqtt_msg=True):
        """
        Moves to the plant's position and positions the arm to measure soil moisture.
        If the soil moisture is below the minimum threshold, it sets the irrigation flow rate to 0.5.
        If the soil moisture is above the maximum threshold, it stops watering by setting the flow rate to 0.0.
        Sends messages via MQTT with the current soil moisture and irrigation flow rate.
        """
        self.move_to(plant.id, send_mqtt_msg=send_mqtt_msg)
        print(f"Watering plant with ID: {plant.id}")
        self.set_arm_position(plant, send_mqtt_msg=send_mqtt_msg)
        moisture = self.soil_moisture_sensor.read_data_at_plant(plant.id)

        if send_mqtt_msg:
            self.send_mqtt_msg(
                TwinComponent.PLANT, {"soil_moisture": moisture * 100}, plant.id + 1
            )

        if moisture < Plant.MIN_MOISTURE:
            self.logger.info(f"Watering with flow rate 0.5.")
            irrigation.set_flow_rate(0.05)
            self.send_mqtt_msg(
                TwinComponent.ROBOT,
                {
                    "action": "water",
                },
            )
        elif moisture >= Plant.MAX_MOISTURE:
            self.logger.info(f"Stopping watering as moisture is too high: {moisture}.")
            irrigation.set_flow_rate(0.0)
        else:
            return
        if send_mqtt_msg:
            self.send_mqtt_msg(
                TwinComponent.IRRIGATION, {"flow_rate": irrigation.read_data() * 100}
            )

    def fertilize_plant(self, plant: Plant, send_mqtt_msg=True):
        """
        Moves to the plant's position and positions the arm to measure soil nutrients.
        If the soil nutrient level is below the minimum threshold, it sets the irrigation flow rate to 0.5.
        If the soil nutrient level is above the maximum threshold, it stops fertilization by setting the flow rate to 0.0.
        Sends messages via MQTT with the current soil nutrient level and irrigation flow rate.
        """
        self.move_to(plant.id, send_mqtt_msg=send_mqtt_msg)
        self.set_arm_position(plant, send_mqtt_msg=send_mqtt_msg)
        nutrient = self.soil_nutrient_sensor.read_data_at_plant(plant.id)

        if send_mqtt_msg:
            self.send_mqtt_msg(
                TwinComponent.PLANT, {"soil_nutrients": nutrient * 100}, plant.id + 1
            )

        if nutrient < Plant.MIN_NUTRIENTS:
            self.logger.info(f"Fertilizing with flow rate 0.5.")
            irrigation.set_flow_rate(0.05)
            self.send_mqtt_msg(
                TwinComponent.ROBOT,
                {
                    "action": "fertilize",
                },
            )
        elif nutrient >= Plant.MAX_NUTRIENTS:
            self.logger.info(
                f"Stopping fertilization as nutrient level is too high: {nutrient}."
            )
            irrigation.set_flow_rate(0.0)
        else:
            return
        if send_mqtt_msg:
            self.send_mqtt_msg(
                TwinComponent.IRRIGATION, {"flow_rate": irrigation.read_data() * 100}
            )

    def move_to(self, position, send_mqtt_msg=True):
        """
        Moves the robot to a specified position.
        Sends a message via MQTT with the new position.
        """
        self.logger.info(f"Moving robot to position: {position}")
        self.chassis.position = position
        if send_mqtt_msg:
            self.send_mqtt_msg(
                TwinComponent.ROBOT,
                {
                    "position": position + 1,
                },
            )

    def move_to_next(self, send_mqtt_msg=True):
        self.move_to(
            (self.chassis.position + 1) % len(self.plants), send_mqtt_msg=send_mqtt_msg
        )

    def set_arm_position(self, plant, send_mqtt_msg=True):
        """
        Sets the arm's position.
        Sends a message via MQTT with the new arm position.
        """
        self.logger.info(f"Setting arm position to: {plant.id}")
        self.arm.position = plant.id
        if send_mqtt_msg:
            self.send_mqtt_msg(
                TwinComponent.ROBOT,
                {
                    "arm_position": str(plant.id),
                },
            )

    def send_mqtt_msg(self, twin_component: TwinComponent, msg, plant_id=None):
        """
        Adds a message to the measurement queue to be sent via MQTT.

        Parameters:
            twin_component (TwinComponent): The component of the twin to which the message belongs.
            msg (dict): The message data to be sent.
            plant_id (int, optional): The ID of the plant if the message is related to a specific plant.
        """
        self.logger.info(f"Sending MQTT message: {msg}")
        self.measurement_queue.put(
            {"component": twin_component, "plant_id": plant_id, "data": msg}
        )

    def run(self):
        """
        Runs the robot's main loop, handling its state and performing actions.
        """

        # send a msg for all plants to initialize the MQTT client
        for plant in self.plants:
            self.send_mqtt_msg(
                TwinComponent.PLANT, self.get_plant_data(plant.id), plant.id + 1
            )

        while True:
            if not self.action_queue.empty():
                action = self.action_queue.get()
                action(self)
            else:
                self.handle_state()

            time.sleep(
                self.cycle_time
            )  # Sleep for a while to simulate time between actions
