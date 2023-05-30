from .event_manager import OSCEventManager


class RandomizedBackground:
    def __init__(self, event_manager: OSCEventManager):
        self.event_manager = event_manager
        self.bin = "forest"
        self.current_layer = "bg1"
        self.current_index = 0
        self.time = 0.0
        self.frequency = 30.0

    def set_bin(self, bin: str):
        self.bin = bin

    def step(self, dt: float):
        self.time += dt
        if self.time < self.frequency:
            return
        self.time = 0.0
        # @todo pick a new cue
        # trigger via LayerSwitch or LayerTransition
        # self.event_manager.add_event()
