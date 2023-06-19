import math
from threading import Lock
import random

from .config import STEPS_PER_SECOND
from .parameter import Parameter
from .scenes import MAIN_SCENES, EVENTS

VELOCITY_THRESHOLD = 0.1  # needs testing


class Simulation:
    """
    The Simulation class represents a simulation environment with a scene and configuration parameters that control the simulation.

    idea: track a forest health variable that determines what scene we are in
    - this variable can be a function of it's pervious state, the time step, and the current parameter values
    - the background, foregrounds, and fx can all be a function of this variable and how it changes over time
    - in addition to changes in the health causing visual changes, parameter changes can also be triggered

    Attributes:
        - scene (str): the current scene of the simulation
        - config (dict): a dictionary of configuration parameters and their corresponding values
        - lock (Lock): a threading lock used to prevent race conditions when updating the configuration
    """

    def __init__(self):
        self.scene = "healthy_forest"
        self.forest_health = Parameter(1.0, lookback=STEPS_PER_SECOND)
        self.config = {
            # this is a parameter controlling the impact of climate change
            "climate_change": {
                "parameter": Parameter(0.0, lookback=STEPS_PER_SECOND),
                "weight": 1.0,
            },
            # this is a paramter controlling the impact of human activity which can be good or bad
            "human_activity": {
                "parameter": Parameter(0.5, lookback=STEPS_PER_SECOND),
                "weight": 1.0,
            },
            # this is a parameter controlling the randomness of fx and events
            "fate": {
                "parameter": Parameter(0.0),
            },
        }
        for param in self.config.keys():
            self.config[param]["parameter"].add_value()
        self.events = ["rain", "storm", "reset"]
        self.lock = Lock()
        self.event_till = None
        self.current_time = 0.0
        self.scene_intensity = 0.0
        self.event_forest_health_effect = 0.0

    def update_config(self, key: str, value: float):
        """Updates a configuration parameter"""
        self.lock.acquire()
        print("Updating", key, "to", value)
        self.config[key]["value"].update_value(value)
        self.lock.release()

    def handle_event(self, event: str, duration=30.0):
        """Set scene to event and determine effect on forest health."""
        self.scene = event
        self.event_till = self.current_time + duration

        if event == "climate_change" or event == "deforestation":
            self.event_forest_health_effect = -0.1

        if event == "storm_forest" and self.forest_health.get_current_value() < 0.77:
            self.event_forest_health_effect = -0.1

        if event == "rain_forest":
            self.event_forest_health_effect = 0.1

    def trigger_event(self, event: str):
        """Trigger a given event."""
        if event not in self.events:
            print("Received unknown event: " + event)
            return

        self.lock.acquire()

        if event == "rain" or event == "storm":
            print("triggering " + event)
            self.handle_event(f"{event}_forest")

        if event == "reset":
            print("reseting")
            self.forest_health = Parameter(1.0, lookback=STEPS_PER_SECOND)
            self.current_time = 0.0

        self.lock.release()

    def get_forest_health(self, dt: float):
        """Computes the current forest health."""
        forest_health = self.forest_health.get_current_value()
        forest_health += (
            self.config["climate_change"]["parameter"].get_current_value()
            * self.config["climate_change"]["weight"]
            * -dt
        )
        forest_health += (
            (0.5 - self.config["human_activity"]["parameter"].get_current_value())
            * self.config["human_activity"]["weight"]
            * dt
        )
        return forest_health

    def trigger_event_on_velocity(
        self, event: str, param: Parameter, value_threshold=0.5
    ):
        """Triggers an event if the param experiences fast changes."""
        value = param.get_current_value()
        velocity = param.get_velocity()
        if abs(velocity) > VELOCITY_THRESHOLD:
            if value > (1.0 - value_threshold) and value > 0.0 and self.scene != event:
                self.handle_event(event, 15)
                self.scene_intensity += 0.1
            elif value < value_threshold and value < 0.0 and self.scene == event:
                self.event_till = None

    def update(self, dt: float):
        self.lock.acquire()

        self.current_time += dt

        # update forest health
        forest_health = self.get_forest_health(dt)
        forest_health += self.event_forest_health_effect
        self.event_forest_health_effect = 0
        forest_health = min(1.0, max(0.0, forest_health))
        self.forest_health.add_value(forest_health)

        # compute scene and scene intensity
        scene_val = (1.0 - forest_health) * len(MAIN_SCENES)
        scene_idx = math.floor(scene_val)
        fate_value = self.config["fate"]["parameter"].get_current_value()
        self.scene_intensity = min(1.0, scene_val - scene_idx + fate_value * 0.5)

        # trigger events on fast control change
        self.trigger_event_on_velocity(
            "climate_change", self.config["climate_change"]["parameter"]
        )
        self.trigger_event_on_velocity(
            "deforestation", self.config["human_activity"]["parameter"], 0.25
        )

        if self.event_till is not None:
            if self.current_time >= self.event_till:
                self.event_till = None
        else:
            fate_roll = random.random()
            if fate_roll < fate_value * 0.0001:
                event = EVENTS[random.randint(0, len(EVENTS) - 1)]
                self.handle_event(event)
            else:
                self.scene = MAIN_SCENES[scene_idx]

        for param in self.config.keys():
            self.config[param]["parameter"].add_value()

        self.lock.release()
