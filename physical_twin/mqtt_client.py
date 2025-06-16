"""
This module provides functionality to connect to and send messages to an MQTT broker in the Ditto protocol format.
"""

from queue import Queue
import paho.mqtt.client as mqtt
import time
import json
from twin_component import TwinComponent

# Namespace of the OpenTwins (Eclipse Ditto) Digital Twin
namespace = "ba"

# Global message queue for MQTT messages
message_queue: Queue = None

# MQTT broker configuration
broker = "localhost"  # MQTT broker address
port = 59973  # MQTT port
topic = "telemetry/"  # Topic where data will be published


def on_connect(client, userdata, flags, rc):
    """
    Prints if the MQTT client successfully connected to the broker.
    """
    if rc == 0:
        print("Successful connection")
    else:
        print(f"Connection failed with code {rc}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect


def set_message_queue(queue):
    global message_queue
    message_queue = queue
    
def set_port(mqtt_port):
    global port
    port = mqtt_port


def send_message(msg):
    """
    Sends a message to the MQTT broker in the Ditto protocol format.
    :param msg: The message to be sent, containing 'component', 'plant_id'(only for plant data), and 'data'.
    """

    twin_name = get_twin_name_for_twin_component(msg["component"])
    if msg["plant_id"] is not None:
        twin_name += f":plant_{msg['plant_id']}"
    formatted_features = features_to_ditto_protocol(msg["data"])
    ditto_msg = to_ditto_protocol(twin_name, formatted_features)

    print(
        f"Publishing message to {topic + namespace + '/' + twin_name}: {json.dumps(ditto_msg)}"
    )
    # Publish the message to the MQTT broker
    client.publish(topic + namespace + "/" + twin_name, json.dumps(ditto_msg))


def features_to_ditto_protocol(features):
    """
    Converts a dictionary of features into the Ditto protocol format.
    :param features: A dictionary where keys are feature names and values are their corresponding values.
    :return: A dictionary formatted for the Ditto protocol.
    """
    features_dict = {}
    for feature, value in features.items():
        features_dict[feature] = {
            "properties": {
                "value": value,
                "time": round(time.time() * 1000),  # Current time in milliseconds
            }
        }
    return features_dict


def get_twin_name_for_twin_component(twin_component: TwinComponent):
    """
    Returns the twin name for a given TwinComponent.
    """
    return twin_component.value


def to_ditto_protocol(twin_name, features):
    """
    Converts the features into the Ditto protocol format for a specific twin.
    :param twin_name: The name of the twin.
    :param features: A dictionary of features to be included in the message.
    :return: A dictionary formatted for the Ditto protocol.
    """
    return {
        "topic": f"{namespace}/{twin_name}/things/twin/commands/merge",
        "headers": {"content-type": "application/merge-patch+json"},
        "path": "/features",
        "value": features,
    }


def run_mqtt_client():
    """
    Starts the MQTT client and connects to the broker.
    This function runs in a loop, checking the message queue for new messages to send.
    If a message is available, it sends the message to the MQTT broker.
    """
    # client.username_pw_set(username, password)
    client.connect(broker, port, 60)

    try:
        while True:
            if message_queue is not None and not message_queue.empty():
                msg = message_queue.get(block=True)
                send_message(msg)

    except KeyboardInterrupt:
        print("Disconnecting MQTT client...")
        client.disconnect()
