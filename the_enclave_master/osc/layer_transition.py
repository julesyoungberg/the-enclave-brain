from .control_fade import ControlFade
from .event_sequence import EventSequence
from .trigger_cue import TriggerCue
from .sleep import OSCSleep


class LayerTransition(EventSequence):
    """A class that defines a sequence of events for transitioning a layer in a media player.
    The class inherits from EventSequence.

    Attributes:
    - layer (str): The name of the layer to transition.
    - cue_bank (str): The name of the cue bank associated with the layer.
    - cue_index (int): The index of the cue to trigger.
    - use_mask (bool): Determines whether or not the transition should use a mask.
    - fade (float): The duration of the fade, in seconds, if any.
    """

    def __init__(
        self, layer: str, cue_bank: str, cue_index: int, use_mask=False, fade=0.0
    ):
        events = []

        if fade > 0.0:
            if use_mask:
                events.append(ControlFade(layer, "mask_opacity", 0.5, 1.0, fade))
            else:
                events.append(ControlFade(layer, "opacity", 1.0, 0.0, fade))

        events.append(
            TriggerCue(
                layer,
                cue_bank,
                cue_index,
            )
        )

        events.append(OSCSleep(6.0))

        if fade > 0:
            if use_mask:
                events.append(ControlFade(layer, "mask_opacity", 1.0, 0.5, fade))
            else:
                events.append(ControlFade(layer, "opacity", 0.0, 1.0, fade))

        super().__init__(events)
