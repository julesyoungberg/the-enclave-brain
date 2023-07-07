import math
import numpy as np
from threading import Lock
import random

from .utils import scale_value
from .config import STEPS_PER_SECOND
from .parameter import Parameter
from .scenes import MAIN_SCENES, SCENES

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
        self.forest_health = Parameter(1.0, lookback=1)
        self.config = {
            # this is a parameter controlling the impact of climate change
            "climate_change": {
                "parameter": Parameter(0.0, lookback=1),
                "weight": 0.005,
            },
            # this is a paramter controlling the impact of human activity which can be good or bad
            "human_activity": {
                "parameter": Parameter(0.0, lookback=1),
                "weight": 0.005,
            },
            # this is a parameter controlling the randomness of fx and events
            "fate": {
                "parameter": Parameter(0.5, lookback=1),
            },
        }
        self.lock = Lock()
        self.event_till = None
        self.event_length = None
        self.current_time = 0.0
        self.scene_intensity = 0.0
        self.event_forest_health_effect = 0.0
        self.has_died = False
        self.has_burned = False
        self.time_since_scene_change = 0

    def param(self, name: str) -> Parameter:
        """Helper for retrieving config params"""
        return self.config[name]["parameter"]

    def print_config(self):
        for key in self.config:
            print(f"{key}={round(self.param(key).get_mean(), 3)}", end="\t")
        print(f"forest_health={self.forest_health.get_current_value()}")

    def update_config(self, key: str, value: float):
        """Updates a configuration parameter"""
        self.lock.acquire()
        if key != "fate":
            value = value * 2.0 - 1.0
        # print("Updating", key, "to", value)
        self.config[key]["parameter"].update_value(value)
        self.lock.release()

    def handle_event(self, event: str, duration=30.0):
        """Set scene to event and determine effect on forest health."""
        if event not in SCENES:
            return
        
        self.scene = event
        self.event_till = self.current_time + duration
        self.event_length = duration
        self.time_since_scene_change = 0

        if event == "climate_change" or event == "deforestation":
            self.event_forest_health_effect = -0.1

        if event == "storm":
            self.event_forest_health_effect = -0.1

        if event == "rain":
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
        forest_health -= (
            self.param("climate_change").get_mean()
            * self.config["climate_change"]["weight"]
            * dt
        )
        forest_health -= (
            self.param("human_activity").get_mean()
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
                scene_intensity = (scene_val - 0.7) / 0.2
        # self.scene_intensity = scene_intensity
        fate_value = self.param("fate").get_mean()
        self.scene_intensity = min(1.0, scene_intensity * 0.7 + fate_value * 0.3)
    
    def update_event_length(self):
        if self.event_length is None:
            return

        scene_config = SCENES[self.scene]
        if "max_length" not in scene_config or "min_length" not in scene_config:
            return
        
        min_length = scene_config["min_length"]
        max_length = scene_config["max_length"]
        old_event_length = self.event_length
        value = self.forest_health.get_current_value()
        if "more_health_is_longer" not in scene_config or not scene_config["more_health_is_longer"]:
            value = 1.0 - value
        # self.event_length = scale_value(value, 0.0, 1.0, min_length, max_length)
        self.event_lenght = value * (max_length - min_length) + min_length
        self.event_till += self.event_length - old_event_length

    def trigger_knob_event(
        self, event: str, param: Parameter, value_threshold=0.25
    ):
        if self.event_till is not None:
            return

        value = param.get_mean()
        velocity = param.get_velocity()
        if np.sign(velocity) != np.sign(value_threshold) or abs(velocity) < VELOCITY_THRESHOLD:
            return
        
        if (
            (value_threshold > 0.0 and value > value_threshold) or
            (value_threshold < 0.0 and value < value_threshold)
        ):
            print(f"event={event}, param_value={value}, velocity={velocity}, value_threshold={value_threshold}")
            print("triggering knob event:", event)
            self.handle_event(event, 30 * (1.0 + abs(value)))

    def trigger_velocity_events(self):
        """Triggers events based on parameter velocity."""
        if self.event_till is not None:
            return

        # trigger events on fast control change
        # self.trigger_event_on_velocity(
        #     "climate_change", self.param("climate_change")
        # )
        # self.trigger_event_on_velocity(
        #     "deforestation", self.param("human_activity"), 0.75
        # )
        # self.trigger_event_on_velocity(
        #     "growing_forest", self.param("human_activity"), 0.25, invert=True
        # )
        # @todo adjust threshold based on fate
        self.trigger_knob_event("storm", self.param("climate_change"), -0.75)
        self.trigger_knob_event("rain", self.param("climate_change"), -0.3)
        self.trigger_knob_event("climate_change", self.param("climate_change"), 0.5)
        self.trigger_knob_event("growing_forest", self.param("human_activity"), -0.5)
        self.trigger_knob_event("deforestation", self.param("human_activity"), 0.5)

    def trigger_probability_event(self, event: str, param: Parameter, roll: float, weight=0.0001):
        """Trigger event based on param probability and roll"""
        if self.event_till is not None:
            return

        value = param.get_mean() * weight
        if roll < value:
            print(f"triggering probability event ({roll} < {value}):", event)
            self.handle_event(event)
            return 0.0

        return roll - value

    def trigger_fate_events(self):
        """Triggers events randomly based on fate."""
        if self.event_till is not None:
            return

        # trigger random events based on fate
        fate_value = self.param("fate").get_mean() * 0.001
        fate_roll = random.random()
        if fate_roll < fate_value:
            fate_events = ["rain", "storm"]
            event = fate_events[random.randint(0, len(fate_events) - 1)]
            print(f"triggering fate event ({fate_roll} < {fate_value}):", event)
            self.handle_event(event)
            return
        # else:
        #     fate_roll -= fate_value

        # fate_roll = self.trigger_probability_event(
        #     "climate_change", self.param("climate_change"), fate_roll
        # )

        # self.trigger_probability_event(
        #     "deforestation", self.param("human_activity"), fate_roll
        # )

    def set_main_scene(self):
        """Sets the main scene if there is no current event"""
        if self.event_till is not None or self.time_since_scene_change < 15.0:
            return

        prev_scene = self.scene
        # trigger time based scenes
        forest_health = self.forest_health.get_current_value()
        if forest_health < 0.2:
            if not self.has_burned:
                self.handle_event("burning_forest", 20)
                self.has_burned = True
            else:
                self.scene = "dead_forest"
                self.has_died = True
        elif forest_health < 0.5:
            if self.has_died or self.has_burned:
                self.handle_event("growing_forest", 20)
                self.has_burned = False
            else:
                self.handle_event("burning_forest", 20)
                self.has_burned = True
        else:
            if self.has_burned:
                self.handle_event("growing_forest", 20)
            else:
                self.scene = "healthy_forest"
            self.has_died = False
            self.has_burned = False

        if self.scene is not prev_scene:
            self.time_since_scene_change = 0

    def commit_config_params(self):
        """Saves current config params for the current frame."""
        for param in self.config.keys():
            self.param(param).update()

    def update(self, dt: float):
        """Main simulation update logic."""
        self.lock.acquire()

        self.current_time += dt
        self.time_since_scene_change += dt

        if self.event_till is not None:
            if self.current_time >= self.event_till:
                self.event_till = None
                self.event_length = None

        self.update_scene_data(dt)

        self.update_event_length()

        self.trigger_velocity_events()

        self.trigger_fate_events()

        self.set_main_scene()

        self.commit_config_params()

        # @todo remove
        # self.randomize_config_params()

        self.lock.release()

    def randomize_config_params(self):
        """Randomize config params for testing"""
        for param_name in self.config:
            next_value = math.sin(self.current_time*5)
            param = self.param(param_name)
            param.update_value(next_value)
            # roll = random.random()
            # if roll < 0.01:
            #     param = self.param(param_name)
            #     value = param.get_mean()
            #     change = (random.random() - 0.5) * 0.2
            #     next_value = min(1.0, max(0.0, value + change))
            #     # print(f"setting value {param_name}:", next_value)
            #     param.update_value(next_value)
