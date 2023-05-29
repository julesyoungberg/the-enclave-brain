from .control_fade import ControlFade
from .event_stack import EventStack
from .event_sequence import EventSequence
from .trigger_cue import TriggerCue
from .sleep import OSCSleep


class LayerSwitch(EventSequence):
    """
    A class that represents a layer switch event sequence.

    Args:
        prev_layer (str): The name of the previous layer to be switched.
        next_layer (str): The name of the next layer to be switched.
        cue_bank (int): The number of the cue to be triggered in the next layer.
        cue_index (int): The index of the cue to be triggered in the next layer.
        fade (float): The fade duration for all fade effects in the sequence.
        use_mask (bool): A flag indicating whether a mask should be used or not.
    """

    def __init__(
        self,
        prev_layer: str,
        next_layer: str,
        cue_bank: str,
        cue_index: int,
        fade=6.0,
        use_mask=False,
    ):
        events = [TriggerCue(next_layer, cue_bank, cue_index), OSCSleep(6.0)]

        if use_mask:
            events.append(ControlFade(next_layer, "mask_opacity", 0.0, 1.0, 0.0))

        events.append(ControlFade(next_layer, "opacity", 0.0, 0.5, fade))

        swap_events = [
            ControlFade(prev_layer, "opacity", 1.0, 0.5, fade),
            ControlFade(next_layer, "opacity", 0.5, 1.0, fade),
        ]

        if use_mask:
            swap_events.append(ControlFade(prev_layer, "mask_opacity", 0.7, 1.0, fade))
            swap_events.append(ControlFade(next_layer, "mask_opacity", 1.0, 0.7, fade))

        events.append(EventStack(swap_events))

        events.append(ControlFade(prev_layer, "opacity", 0.5, 0.0, fade))

        super().__init__(events)
