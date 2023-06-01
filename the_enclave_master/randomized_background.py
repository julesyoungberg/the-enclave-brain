import random

from .osc.addresses import MADMAPPER_ADDRESSES
from .osc.events import OSCEventManager
from .osc.transitions import TriggerCue


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

        self.current_layer = f"bg{random.randint(1, 2)}"
        self.current_index = random.randint(
            0, len(MADMAPPER_ADDRESSES[self.current_layer]["cues"][self.bin]) - 1
        )

        self.event_manager.add_event()

        # @todo pick a new cue
        # trigger via LayerSwitch or LayerTransition
        # self.event_manager.add_event()
