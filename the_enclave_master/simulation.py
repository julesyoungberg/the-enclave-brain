from threading import Lock


class Simulation:
    """
    The Simulation class represents a simulation environment with a scene and configuration parameters that control the simulation.

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
            "polution": 0.0,
            "deforestation": 0.0,
            "new_trees": 0.0,
        }
        self.lock = Lock()

    def update_config(self, key: str, value: float):
        self.lock.acquire()
        print("Updating", key, "to", value)
        self.config[key] = value
        self.lock.release()

    def update(self, dt: float):
        self.lock.acquire()
        # @todo update simulation by timestep
        self.scene = "scene1"
        self.lock.release()

    def get_scene(self) -> str:
        return self.scene
