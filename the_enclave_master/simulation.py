from threading import Lock

class Simulation:
    def __init__(self):
        self.scene = 'scene1'
        self.config = {
            'polution': 0.0,
            'deforestation': 0.0,
            'new_trees': 0.0,
        }
        self.lock = Lock()

    def update_config(self, key: str, value: float):
        self.lock.acquire()
        print("Updating", key, "to", value)
        self.config[key] = value
        self.lock.release()

    def update(self):
        self.lock.acquire()
        # @todo update simulation by timestep
        self.scene = 'scene2'
        self.lock.release()

    def get_scene(self) -> str:
        return self.scene
