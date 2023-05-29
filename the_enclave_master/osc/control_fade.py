from . import addresses
from .transition import OSCTransition


class ControlFade(OSCTransition):
    """Represents a control transition for a layer."""

    def __init__(
        self, layer: str, control: str, start: float, end: float, duration: float
    ):
        address = addresses.control(layer, control)
        super().__init__(address, start, end, duration)
