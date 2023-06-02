import random

from .osc.addresses import MADMAPPER_CONFIG
from .osc.events import OSCEventManager
from .osc.transitions import LayerSwitch, LayerTransition
from .scenes import SCENES


class LayerRandomizer:
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

    def __init__(
        self, event_manager: OSCEventManager, scene="healthy_forest", layer_type="bg"
    ):
        self.event_manager = event_manager
        self.scene = scene
        self.current_bin = "forest"
        self.layer_type = layer_type
        self.current_layer = f"{layer_type}1"
        self.current_index = 0
        self.time = 0.0
        self.frequency = 30.0  # seconds
        self.update()

    def update(self, prev_layer=None):
        # randomly select new layer and cue
        layer_index = random.randint(1, 2)
        self.current_layer = f"{self.layer_type}{layer_index}"
        bins = SCENES[self.scene][self.layer_type]
        self.current_bin = bins[random.randint(0, len(bins) - 1)]

        if self.current_bin not in MADMAPPER_CONFIG[self.current_layer]["cues"]:
            if layer_index == 1:
                self.current_layer = f"{self.layer_type}2"
            else:
                self.current_layer = f"{self.layer_type}1"

        self.current_index = random.randint(
            0,
            len(MADMAPPER_CONFIG[self.current_layer]["cues"][self.current_bin]) - 1,
        )

        if prev_layer is not None and prev_layer != self.current_layer:
            self.event_manager.add_event(
                LayerSwitch(self.current_layer, self.current_bin, self.current_index)
            )
        else:
            self.event_manager.add_event(
                LayerTransition(
                    self.current_layer, self.current_bin, self.current_index
                )
            )

    def set_bin(self, bin: str):
        self.bin = bin

    def step(self, dt: float):
        self.time += dt
        if self.time < self.frequency:
            return

        self.time = 0.0

        self.update()
