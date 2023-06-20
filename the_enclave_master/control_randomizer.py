import random

from .osc.events import OSCEventManager
from .osc.transitions import ControlFade


class ControlRandomizer:
    """
    The ControlRandomizer class is used to randomize a control parameter for layer special effects, based on a given intensity value.
    The class takes an instance of OSCEventManager, the layer name, control name, as well as optional minimum and maximum values for the control range, as initialization arguments.

    The update method updates the current value of the control parameter by generating a new random value within the range and intensity constraints, and applies a fade transition to the new value over a random fade time (based on the intensity value).
    The generated ControlFade instance is added to the OSCEventManager's event queue for execution.

    Note that the intensity value is defined within the ControlRandomizer instance and can be changed by the user.
    """

    def __init__(
        self, event_manager: OSCEventManager, layer: str, control: str, min=0.0, max=1.0
    ):
        self.min = min
        self.max = max
        self.intensity = 0.5
        self.event_manager = event_manager
        self.layer = layer
        self.control = control
        self.time = 0.0
        self.current_event = None
        self.end_value = None

    def update(self, dt: float):
        self.time += dt

        if self.current_event is not None and not self.current_event.done:
            return

        start_value = self.end_value or self.min
        range = self.max - self.min
        # force stronger fx based on intensity
        mx = self.max - range * 0.5 * (1.0 - self.intensity)
        mn = self.min + range * 0.5 * self.intensity
        range = (mx - mn) * (self.intensity * 0.5 + 0.25)
        self.end_value = max(
            mn,
            min(
                mx,
                start_value + random.random() * range - range * 0.5,
            ),
        )
        fade_time = random.random() * 10.0 * (1.0 - self.intensity * 0.5)
        self.current_event = ControlFade(
            self.layer, self.control, start_value, self.end_value, fade_time
        )
        self.event_manager.add_event(self.current_event)
