# Digital Twins for the Automation of a Green House

Repository for my Bachelor's Thesis "Digital Twins for the Automation of a Green House"

## Overview

### Physical Twin

Simulation of a robot that connects to the digital twin. Simulates working on greenhouse horticulture tasks, cycling through the plants. The robot reports its data to the digital twin via MQTT and is controlled via HTTP. 

The plants are also simulated and updated each simulation cycle.

### Digital Twin

OpenTwins digital twin of the robot, the greenhouse environment, all the plants and the irrigation system.

### Unity Visualization

Unity visualization of the greenhouse. Visualizes robot movement and actions as well as planth growth and recommended actions for each plant. Built with WebGL and integrated into the Grafana dashboard.

The WebGL build can be opened via `index.html` in the `unity_webgl_build` directory using a web server (e.g. VS Code Live Server) to see a demo of the visualization.

## Installation

Clone the repository to your local machine

Install OpenTwins and its dependencies, as per [the OpenTwins Quickstart Guide](https://ertis-research.github.io/opentwins/docs/quickstart).

Here, an installation via Helm is assumed, but you can also install OpenTwins manually if you prefer.

By default the Grafana Dashboard expects the Unity WebGL build files at "http://localhost:8080/unity/Build/[FILE_NAME]".

Make sure to put the Unity WebGL build files in that location (from the "http_server.py" root directory), or change the URL in the Grafana Dashboard settings.

When first starting the digital twin, import the provided Grafana Dashboard JSON file (from the "grafana" directory) into your Grafana instance by navigating to "Dashboards" -> "New" -> "Import" and uploading the JSON file.

JSON files for the twin types are provided in the "digital_twin" directory, which can be used to create the twins. After creating the types, add the desired amount of plants as children in the ""Hierarchy" tab of the plant container type (default in this project: 20).

## Usage

To start the digital twin, follow the steps from [the OpenTwins Guide](https://ertis-research.github.io/opentwins/docs/installation/using-helm#configuration).

Here, deploying the twin via Minikube is assumed.

For convenience, a tasks.json file is provided to run the required commands to start the digital twin (from Visual Studio Code). 

>**Note:** You still need to manually enter the URLs for Eclipse Ditto and Ditto Extended API in Grafana.

>**Note:** It was created for and only tested in a Windows 11 environment.

To run the robot simulation run main.py in the "physical_twin" directory, make sure to pass the correct mqtt port (from minikube/kubernetes) as an argument, e.g. `python main.py --mqtt_port 1883`. For more info on options run python main.py --help.
