from robot import Robot
import simulation
from model.environment import Environment
from model.plant import Plant
import http_server as http_server
import mqtt_client as mqtt_client
from queue import Queue
import threading
from robot_state import RobotState
import argparse


def main():
    """
    Main function to initialize and run the digital twin simulation.
    This function sets up the environment, plants, robot, MQTT client, and HTTP server,
    and starts the simulation cycle.
    The simulation, mqtt client, and HTTP server run in separate threads to allow for concurrent operations.
    """

    parser = argparse.ArgumentParser(description="Run the digital twin simulation.")
    parser.add_argument("--mqtt_port", type=int, required=True, help="Port for the MQTT client")
    parser.add_argument("--plant_amount", type=int, default=20, help="Number of plants (default: 20)")
    parser.add_argument("--simulation_cycle_time", type=int, default=60, help="Cycle time in seconds (default: 60)")
    parser.add_argument("--robot_cycle_time", type=int, default=60, help="Robot cycle time in seconds (default: 60)")
    args = parser.parse_args()

    mqtt_port = args.mqtt_port
    plant_amount = args.plant_amount
    simulation_cycle_time = args.simulation_cycle_time
    robot_cycle_time = args.robot_cycle_time
    
    environment = Environment()

    plants = [
        Plant(id=i) for i in range(0, plant_amount)
    ]  

    # message queue for measurements, the robot puts measurements into this queue
    # and the MQTT client reads from it to publish to the MQTT broker
    measurement_queue = Queue()

    robot = Robot(plants=plants, measurement_queue=measurement_queue,cycle_time=robot_cycle_time)

    robot.set_state(RobotState.AUTO)  # Set the robot to auto mode

    simulation.initialize(environment, plants, simulation_cycle_time)
    threading.Thread(
        target=simulation.run_simulation, daemon=True
    ).start()  # Start the simulation cycle in a separate thread

    mqtt_client.set_message_queue(measurement_queue)
    mqtt_client.set_port(mqtt_port)  # Set the MQTT port
    threading.Thread(target=mqtt_client.run_mqtt_client, daemon=True).start()

    threading.Thread(
        target=http_server.run_http_server, args=(robot,), daemon=True
    ).start()

    robot.run()  # Start the robot's main loop


if __name__ == "__main__":
    main()
