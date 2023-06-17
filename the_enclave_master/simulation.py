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
        - get_scene() -> str: returns the current scene of the simulation
    """

    def __init__(self):
        self.scene = "scene1"
        self.config = {
            "climate_change": 0.0,  # this is a parameter controlling the impact of climate change
            "human_activity": 0.0,  # this is a paramter controlling the impact of human activity which can be good or bad
            "fate": 0.0,  # this is a parameter controlling the randomness of fx and events
        }
        self.events = ["rain", "storm", "reset"]
        self.lock = Lock()

    def update_config(self, key: str, value: float):
        self.lock.acquire()
        print("Updating", key, "to", value)
        self.config[key] = value
        self.lock.release()

    def trigger_event(self, event: str):
        if event not in self.events:
            print("Received unknown event: " + event)
            return

        if event == "rain" or event == "storm":
            print("triggering " + event)
            # @todo trigger scene

        if event == "reset":
            print("reseting")
            # @todo reset time

    def update(self, dt: float):
        self.lock.acquire()
        # @todo update simulation by timestep
        self.scene = "scene1"
        self.lock.release()

    def get_scene(self) -> str:
        return self.scene
