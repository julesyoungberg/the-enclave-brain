from threading import Lock

class Simulation:
    def __init__(self):
        # @todo set up variables that represent sim
        self.scene = 0
        self.config = {}
        self.lock = Lock()

    def update_config(self, key: str, value: float):
        self.lock.acquire()
        print("Updating", key, "to", value)
        self.config[key] = value
        self.lock.release()

    def update(self):
        self.lock.acquire()
        # @todo update simulation by timestep
        self.scene = 1
        self.lock.release()

    def get_scene(self) -> int:
        return self.scene
