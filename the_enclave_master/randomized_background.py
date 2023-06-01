import random

from .osc.addresses import MADMAPPER_ADDRESSES
from .osc.events import OSCEventManager
from .osc.transitions import TriggerCue


class RandomizedBackground:
    """
    The RandomizedBackground class is used to manage the randomized backgrounds and trigger events periodically.

    Attributes:
        event_manager (OSCEventManager): The event manager that triggers cue events.
        bin (str): The current cue bin holding the background videos.
        current_layer (str): The current background layer being displayed.
        current_index (int): The current index of the cue for the current layer.
        time (float): The time elapsed since the last cue event was triggered.
        frequency (float): The frequency of cue events in seconds.
    """

    def __init__(self, event_manager: OSCEventManager):
        self.event_manager = event_manager
        self.bin = "forest"
        self.current_layer = "bg1"
        self.current_index = 0
        self.time = 0.0
        self.frequency = 30.0  # seconds

    def set_bin(self, bin: str):
        self.bin = bin

    def step(self, dt: float):
        self.time += dt
        if self.time < self.frequency:
            return

        self.time = 0.0

        # randomly select new layer and cue
        self.current_layer = f"bg{random.randint(1, 2)}"
        self.current_index = random.randint(
            0, len(MADMAPPER_ADDRESSES[self.current_layer]["cues"][self.bin]) - 1
        )

        self.event_manager.add_event(
            TriggerCue(self.current_layer, self.bin, self.current_index)
        )
