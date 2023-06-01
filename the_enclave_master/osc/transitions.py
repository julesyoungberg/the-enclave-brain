from . import addresses
from .events import OSCEvent, EventSequence, OSCSleepEvent


class TriggerCue(OSCEvent):
    """Represents an instantaneous OSC that triggers a cue for a specific layer, cue bank, and index."""

    def __init__(self, layer: str, cue_bin: str, cue_index: int):
        address = addresses.layer_cue(layer, cue_bin, cue_index)
        super().__init__(address)

    def step(self, dt: float):
        super().step(dt, 1.0)


class OSCTransition(OSCEvent):
    """Represents the transition of an OSC message's parameter value over time.

    Attributes:
        start (float): The start value of the parameter.
        end (float): The end value of the parameter.
    """

    def __init__(self, address: str, start: float, end: float, duration: float):
        super().__init__(address, duration)
        self.start = start
        self.end = end

    def step(self, dt: float):
        """Calculates the current parameter value based on time and sends an OSC message with the current value to the specified address.

        Args:
            dt (float): The time elapsed since the last call to step.
        """
        value = ((self.time / self.duration) * (self.end - self.start) + self.start,)
        super().step(dt, value)


class ControlFade(OSCTransition):
    """Represents a control transition for a layer."""

    def __init__(
        self, layer: str, control: str, start: float, end: float, duration: float
    ):
        address = addresses.control(layer, control)
        super().__init__(address, start, end, duration)


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

        events.append(OSCSleepEvent(6.0))

        if fade > 0:
            if use_mask:
                events.append(ControlFade(layer, "mask_opacity", 1.0, 0.5, fade))
            else:
                events.append(ControlFade(layer, "opacity", 0.0, 1.0, fade))

        super().__init__(events)
