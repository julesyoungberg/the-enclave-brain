import math
from threading import Lock


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

    Methods:
        - update_config(key: str, value: float) -> None: updates the value of a configuration parameter with a given key
        - update(dt: float) -> None: updates the simulation by one timestep
    """

    def __init__(self):
        self.scene = "healthy_forest"
        self.forest_health = 1.0
        self.config = {
            # this is a parameter controlling the impact of climate change
            "climate_change": {
                "value": 0.0,
                "prev_value": 0.0,
                "weight": 1.0,
            },
            # this is a paramter controlling the impact of human activity which can be good or bad
            "human_activity": {
                "value": 0.0,
                "prev_value": 0.0,
                "weight": 1.0,
            },
            # this is a parameter controlling the randomness of fx and events
            "fate": {
                "value": 0.0,
                "prev_value": 0.0,
            },
        }
        self.events = ["rain", "storm", "reset"]
        self.lock = Lock()
        self.event_till = None
        self.current_time = 0.0
        self.scene_intensity = 0.0

    def update_config(self, key: str, value: float):
        self.lock.acquire()
        print("Updating", key, "to", value)
        self.config[key]["value"] = value
        self.lock.release()

    def trigger_event(self, event: str):
        self.lock.acquire()
        if event not in self.events:
            print("Received unknown event: " + event)
            return

        if event == "rain" or event == "storm":
            print("triggering " + event)
            self.scene = f"{event} forest"
            self.event_till = self.current_time + 10.0

        if event == "reset":
            print("reseting")
            self.forest_health = 1.0
            self.current_time = 0.0

        self.lock.release()

    def update(self, dt: float):
        self.current_time += dt
        self.lock.acquire()
        self.forest_health += (
            self.config["climate_change"]
            * self.config["climate_change"]["weight"]
            * -dt
        )
        self.forest_health += (
            (0.5 - self.config["human_activity"])
            * self.config["human_activity"]["weight"]
            * dt
        )
        self.forest_health = math.min(1.0, math.max(0.0, self.forest_health))
        scene_idx = (1.0 - self.forest_health) * 4.0
        self.scene_intensity = math.factorial(scene_idx)
        if self.event_till is not None:
            if self.current_time >= self.event_till:
                self.event_till = None
        else:
            self.scene = [
                "healthy_forest",
                "deforestation",
                "burning_forest",
                "dead_forest",
            ][math.floor(scene_idx)]
        # @todo set fx intensity based on distance to next scene
        for control in ["climate_change", "human_activity", "fate"]:
            self.config[control]["prev_value"] = self.config[control]["value"]
        self.lock.release()
