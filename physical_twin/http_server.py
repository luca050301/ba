import socketserver
import http.server
from robot import Robot
from urllib.parse import parse_qs, urlparse
import re
from robot import RobotState

PORT = 8000


class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    Custom request handler that adds CORS headers and handles specific robot and plant actions.
    Also serves the Unity WebGL build files for the grafana panel.
    """

    def __init__(self, robot: Robot,action_queue, *args, **kwargs):
        self.robot = robot
        self.action_queue = action_queue # queue for actions to be performed by the robot
        super().__init__(*args, **kwargs)

    def end_headers(self):
        """
        Override end_headers to add CORS headers.
        """
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        super().end_headers()

    def do_OPTIONS(self):
        """
        Handle CORS preflight requests.
        """
        self.send_response(204)
        self.end_headers()

    def do_POST(self):
        """
        Handle POST requests for robot and plant actions.
        """
        # Robot Path: Endpoints to move the robot or set its state for continuous actions (/robot/{state})
        if self.path.startswith("/robot/move"):
            self.handle_post_robot_move()
        elif self.path == "/robot/harvest":
            self.handle_post_robot_harvest()
        elif self.path == "/robot/seed":
            self.handle_post_robot_seed()
        elif self.path == "/robot/water":
            self.handle_post_robot_water()
        elif self.path == "/robot/fertilize":
            self.handle_post_robot_fertilize()
        elif self.path == "/robot/idle":
            self.handle_post_robot_idle()
        elif self.path == "/robot/monitor":
            self.handle_post_robot_monitor()
        elif self.path == "/robot/auto":
            self.handle_post_robot_auto()
        # Plant Path: Endpoints to perform one-time actions on a plant specified by its ID path parameter (/plant/{id}/{action})
        elif self.path.startswith("/plant/") and self.path.endswith("/water"):
            self.handle_post_plant_water()
        elif self.path.startswith("/plant/") and self.path.endswith("/fertilize"):
            self.handle_post_plant_fertilize()
        elif self.path.startswith("/plant/") and self.path.endswith("/harvest"):
            self.handle_post_plant_harvest()
        elif self.path.startswith("/plant/") and self.path.endswith("/seed"):
            self.handle_post_plant_seed()
        elif self.path.startswith("/plant/") and self.path.endswith("/monitor"):
            self.handle_post_plant_monitor()
        else:
            self.respond(404, "Not Found")

    def handle_post_robot_move(self):
        """
        Handles the robot move request by extracting the position from the query parameters and sets the robot's position.
        """
        query = urlparse(self.path).query
        params = parse_qs(query)
        i = params.get("i", [None])[0]
        if i is not None:
            #self.robot.move_to(int(i) - 1)
            self.action_queue.put(
                lambda robot: robot.move_to(int(i) - 1)
            )

        self.respond_ok("moved to plant " + str(i))

    def handle_post_robot_harvest(self):
        """
        Sets the robot's state to harvesting.
        """
        self.robot.set_state(RobotState.HARVESTING)

        self.respond_ok("Robot is harvesting")

    def handle_post_robot_seed(self):
        """
        Sets the robot's state to seeding.
        """
        self.robot.set_state(RobotState.SEEDING)

        self.respond_ok("Robot is seeding")

    def handle_post_robot_water(self):
        """
        Sets the robot's state to watering.
        """
        self.robot.set_state(RobotState.WATERING)

        self.respond_ok("Robot is watering")

    def handle_post_robot_fertilize(self):
        """
        Sets the robot's state to fertilizing.
        """
        self.robot.set_state(RobotState.FERTILIZING)

        self.respond_ok("Robot is fertilizing")

    def handle_post_robot_idle(self):
        """
        Sets the robot's state to idle.
        """
        self.robot.set_state(RobotState.IDLE)

        self.respond_ok("Robot is idle")

    def handle_post_robot_monitor(self):
        """
        Sets the robot's state to monitoring.
        """
        self.robot.set_state(RobotState.MONITORING)

        self.respond_ok("Robot is monitoring")

    def handle_post_robot_auto(self):
        """
        Sets the robot's state to auto mode.
        """
        self.robot.set_state(RobotState.AUTO)

        self.respond_ok("Robot is in auto mode")

    def handle_post_plant_water(self):
        """
        Handles the plant watering request by extracting the plant ID from the path and watering the specified plant.
        """
        plant_id = self.plant_id_from_path()
        if plant_id is None:
            self.respond(400, "Invalid request path")
            return
        self.action_queue.put(
            lambda robot: robot.water_plant(robot.plants[plant_id - 1])
        )
        print("CALLED FOR PLANT ID:", plant_id)
        #self.robot.water_plant(self.robot.plants[plant_id - 1])

        self.respond_ok(f"Watered plant {plant_id}")

    def handle_post_plant_fertilize(self):
        """
        Handles the plant fertilizing request by extracting the plant ID from the path and fertilizing the specified plant.
        """
        plant_id = self.plant_id_from_path()
        if plant_id is None:
            self.respond(400, "Invalid request path")
            return
        #self.robot.fertilize_plant(self.robot.plants[plant_id - 1])
        self.action_queue.put(
            lambda robot: robot.fertilize_plant(robot.plants[plant_id - 1])
        )

        self.respond_ok(f"Fertilized plant {plant_id}")

    def handle_post_plant_harvest(self):
        """
        Handles the plant harvesting request by extracting the plant ID from the path and harvesting the specified plant.
        """
        plant_id = self.plant_id_from_path()
        if plant_id is None:
            self.respond(400, "Invalid request path")
            return
        #self.robot.harvest_plant(self.robot.plants[plant_id - 1])
        self.action_queue.put(
            lambda robot: robot.harvest_plant(robot.plants[plant_id - 1])
        )

        self.respond_ok(f"Harvested plant {plant_id}")

    def handle_post_plant_seed(self):
        """
        Handles the plant seeding request by extracting the plant ID from the path and seeding the specified plant.
        """
        plant_id = self.plant_id_from_path()
        if plant_id is None:
            self.respond(400, "Invalid request path")
            return
        #self.robot.seed_plant(self.robot.plants[plant_id - 1])
        self.action_queue.put(
            lambda robot: robot.seed_plant(robot.plants[plant_id - 1])
        )

        self.respond_ok(f"Seeded plant {plant_id}")

    def handle_post_plant_monitor(self):
        """
        Handles the plant monitoring request by extracting the plant ID from the path and monitoring the specified plant.
        """
        plant_id = self.plant_id_from_path()
        if plant_id is None:
            self.respond(400, "Invalid request path")
            return
        #self.robot.monitor_plant(plant_id - 1)
        self.action_queue.put(
            lambda robot: robot.monitor_plant(plant_id - 1)
        )

        self.respond_ok(f"Monitored plant {plant_id}")

    def plant_id_from_path(self):
        """
        Extracts the plant ID from the request path using regex.
        """
        match = re.match(
            r"^/plant/(\d+)/(water|fertilize|harvest|seed|monitor)$", self.path
        )
        if match:
            return int(match.group(1))
        else:
            return None

    def respond_ok(self, message: str):
        """
        Sends a 200 OK response with the given message.
        """
        self.respond(200, message)

    def respond(self, status_code: int, message: str):
        """
        Sends a response with the given status code and message.
        """
        self.send_response(status_code)
        self.end_headers()
        self.wfile.write(message.encode())


def make_handler(robot,action_queue):
    """
    Factory function to create a custom request handler for the HTTP server.
    Args:
        robot (Robot): The Robot instance to handle requests for.
    Returns:
        CustomHandler: A custom request handler class that extends CORSRequestHandler.
    """

    class CustomHandler(CORSRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(robot,action_queue, *args, **kwargs)

    return CustomHandler


def run_http_server(robot: Robot,action_queue):
    """
    Starts the HTTP server.
    """
    Handler = make_handler(robot, action_queue)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        httpd.serve_forever()


if __name__ == "__main__":
    """
    Main entry point to start the HTTP server.
    """
    run_http_server()
