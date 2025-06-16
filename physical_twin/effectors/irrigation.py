"""
This module simulates an irrigation system
"""

_flow_rate = 0.0  # Flow rate in liters per minute


def read_data():
    """
    Reads data from the irrigation system.
    Returns:
        float: The current flow rate of the irrigation system in liters per minute.
    """
    return _flow_rate


def set_flow_rate(flow_rate):
    global _flow_rate
    _flow_rate = flow_rate
