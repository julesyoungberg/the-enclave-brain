import random

from .osc.addresses import MADMAPPER_CONFIG, is_one_shot
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
        frequency (float): The frequency of cue events in milliseconds.
    """

    def __init__(
        self, event_manager: OSCEventManager, scene="healthy_forest", layer_type="bg"
    ):
        self.event_manager = event_manager
        self.scene = scene
        self.current_bin = "forest"
        self.layer_type = layer_type
        self.current_layer = None
        self.current_index = 0
        self.time = 0.0
        self.frequency = 30.0  # seconds
        self.update_layer()

    def update_layer(self):
        # randomly select new layer and cue
        was_one_shot = False
        if self.current_layer is not None:
            was_one_shot = is_one_shot(
                self.current_layer, self.current_bin, self.current_index
            )

        prev_layer = self.current_layer
        prev_bin = self.current_bin
        prev_index = self.current_index

        cues = []

        for layer_index in range(2):
            layer_name = self.layer_type + str(layer_index + 1)
            bins = SCENES[self.scene][self.layer_type]
            for bin in bins:
                if bin not in MADMAPPER_CONFIG[layer_name]["cues"]:
                    continue
                for cue in MADMAPPER_CONFIG[layer_name]["cues"][bin]:
                    cues.append(
                        {
                            "layer_index": layer_index + 1,
                            "bin": bin,
                            "cue": cue,
                        }
                    )

        cue = cues[random.randint(0, len(cues) - 1)]

        layer_index = cue["layer_index"]
        self.current_layer = f"{self.layer_type}{layer_index}"
        self.current_bin = cue["bin"]
        self.current_indx = cue["cue"]

        if prev_layer is not None and prev_layer != self.current_layer:
            self.event_manager.add_event(
                LayerSwitch(
                    prev_layer,
                    self.current_layer,
                    self.current_bin,
                    self.current_index,
                    fade=6.0,
                    use_mask=self.layer_type == "bg",
                    prev_was_one_shot=was_one_shot,
                )
            )
        elif (
            prev_layer is None
            or self.current_bin != prev_bin
            or self.current_index != prev_index
        ):
            self.event_manager.add_event(
                LayerTransition(
                    self.current_layer,
                    self.current_bin,
                    self.current_index,
                    # @todo consider taking this from the cue config - some foregrounds might not need the fade
                    fade=0.0
                    if self.layer_type == "bg" and prev_layer is not None
                    else 6.0,
                    prev_was_one_shot=was_one_shot,
                )
            )

    def set_bin(self, bin: str):
        self.bin = bin

    def update(self, dt: float):
        self.time += dt
        if self.time < self.frequency:
            return

        self.time = 0.0
        self.update_layer()
