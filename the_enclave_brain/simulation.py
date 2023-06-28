import math
from threading import Lock
import random

from .config import STEPS_PER_SECOND
from .parameter import Parameter
from .scenes import MAIN_SCENES, EVENTS, SCENES

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
        self.scene = MAIN_SCENES[0]
        self.forest_health = Parameter(1.0, lookback=STEPS_PER_SECOND)
        self.config = {
            # this is a parameter controlling the impact of climate change
            "climate_change": {
                "parameter": Parameter(0.5, lookback=STEPS_PER_SECOND),
                "weight": 0.01,
            },
            # this is a paramter controlling the impact of human activity which can be good or bad
            "human_activity": {
                "parameter": Parameter(0.5, lookback=STEPS_PER_SECOND),
                "weight": 0.01,
            },
            # this is a parameter controlling the randomness of fx and events
            "fate": {
                "parameter": Parameter(0.5),
            },
        }
        self.lock = Lock()
        self.event_till = None
        self.current_time = 0.0
        self.scene_intensity = 0.0
        self.event_forest_health_effect = 0.0

    def param(self, name: str) -> Parameter:
        """Helper for retrieving config params"""
        return self.config[name]["parameter"]

    def update_config(self, key: str, value: float):
        """Updates a configuration parameter"""
        self.lock.acquire()
        print("Updating", key, "to", value)
        self.config[key]["value"].update_value(value)
        self.lock.release()

    def handle_event(self, event: str, duration=30.0):
        """Set scene to event and determine effect on forest health."""
        if event not in SCENES:
            return

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
        self.lock.acquire()

        if event == "reset":
            self.forest_health = Parameter(1.0, lookback=STEPS_PER_SECOND)
            self.current_time = 0.0
        else:
            self.handle_event(event)

        self.lock.release()

    def get_forest_health(self, dt: float):
        """Computes the current forest health."""
        forest_health = self.forest_health.get_current_value()
        forest_health += (
            self.param("climate_change").get_current_value()
            * self.config["climate_change"]["weight"]
            * -dt
        )
        forest_health += (
            (0.5 - self.param("human_activity").get_current_value())
            * self.config["human_activity"]["weight"]
            * dt
        )
        return forest_health

    def update_scene_data(self, dt: float):
        """Updates forest health and scene intensity"""
        forest_health = self.get_forest_health(dt)
        forest_health += self.event_forest_health_effect
        self.event_forest_health_effect = 0
        forest_health = min(1.0, max(0.0, forest_health))
        self.forest_health.update(forest_health)

        # compute scene and scene intensity
        scene_val = 1.0 - forest_health
        scene_intensity = scene_val / 0.5
        if scene_intensity > 1.0:
            scene_intensity = (scene_val - 0.5) / 0.3
            if scene_intensity > 1.0:
                scene_intensity = (scene_val - 0.8) / 0.2
        fate_value = self.param("fate").get_current_value()
        self.scene_intensity = min(1.0, scene_intensity + fate_value * 0.5)

    def trigger_event_on_velocity(
        self, event: str, param: Parameter, value_threshold=0.5
    ):
        """Triggers an event if the param experiences fast changes."""
        value = param.get_current_value()
        velocity = param.get_velocity()
        if abs(velocity) > VELOCITY_THRESHOLD:
            if value > value_threshold and self.scene != event:
                self.handle_event(event, 30 * (1.0 + value))
                self.scene_intensity += 0.1
            elif value < value_threshold and self.scene == event:
                self.event_till = None

    def trigger_velocity_events(self):
        """Triggers events based on parameter velocity."""
        if self.event_till is not None:
            return

        # trigger events on fast control change
        self.trigger_event_on_velocity(
            "climate_change", self.param("climate_change")
        )
        self.trigger_event_on_velocity(
            "deforestation", self.param("human_activity"), 0.75
        )

    def trigger_probability_event(self, event: str, param: Parameter, roll: float):
        """Trigger event based on param probability and roll"""
        value = param.get_current_value() * 0.001
        if roll < value:
            self.handle_event(event)
            return 0.0

        return roll - value

    def trigger_fate_events(self):
        """Triggers events randomly based on fate."""
        if self.event_till is not None:
            return

        # trigger random events based on fate
        fate_value = self.param("fate").get_current_value() * 0.01
        fate_roll = random.random()
        if fate_roll < fate_value:
            event = EVENTS[random.randint(0, len(EVENTS) - 1)]
            self.handle_event(event)
            return
        else:
            fate_roll -= fate_value

        fate_roll = self.trigger_probability_event(
            "climate_change", self.param("climate_change"), fate_roll
        )

        self.trigger_probability_event(
            "deforestation", self.param("human_activity"), fate_roll
        )

    def set_main_scene(self):
        """Sets the main scene if there is no current event"""
        if self.event_till is not None:
            return

        # trigger time based scenes
        forest_health = self.forest_health.get_current_value()
        health_change = self.forest_health.get_change()
        if forest_health < 0.2:
            self.scene = MAIN_SCENES[2]
        elif forest_health < 0.5:
            if health_change < 0.0:
                self.scene = MAIN_SCENES[1]
            else:
                self.scene = MAIN_SCENES[3]
        else:
            self.scene = MAIN_SCENES[0]

    def commit_config_params(self):
        """Saves current config params for the current frame."""
        print("\n\n")
        for param in self.config.keys():
            print(f"commiting {param}: {self.param(param).get_current_value()}")
            self.param(param).update()

    def update(self, dt: float):
        """Main simulation update logic."""
        self.lock.acquire()

        self.current_time += dt

        if self.event_till is not None:
            if self.current_time >= self.event_till:
                self.event_till = None

        self.update_scene_data(dt)

        self.trigger_velocity_events()

        self.trigger_fate_events()

        self.set_main_scene()

        self.commit_config_params()

        # @todo remove
        self.randomize_config_params()

        self.lock.release()

    def randomize_config_params(self):
        """Randomize config params for testing"""
        for param_name in self.config:
            roll = random.random()
            if roll < 0.01:
                param = self.param(param_name)
                value = param.get_current_value()
                change = (random.random() - 0.5) * 0.1
                next_value = min(1.0, max(0.0, value + change))
                param.update_value(next_value)
