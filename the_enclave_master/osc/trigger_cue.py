from . import addresses
from .event import OSCEvent


class TriggerCue(OSCEvent):
    """Represents an instantaneous OSC that triggers a cue for a specific layer, cue bank, and index."""

    def __init__(self, layer: str, cue_bank: str, cue_index: int):
        address = addresses.layer_cue(layer, cue_bank, cue_index)
        super().__init__(address)

    def step(self, dt: float):
        super().step(dt, 1.0)
