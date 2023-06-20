from .control_randomizer import ControlRandomizer
from .osc.events import OSCEventManager


class LayerFXControl:
    """
    The LayerFXControl class manages the visualization of special effects on a given layer.
    It takes an OSCEventManager instance and the name of the layer as arguments at initialization.
    The class also creates three ControlRandomizer instances for controlling the fx_amount, feedback_amount, and feedback_fx_amount attributes.

    The set_intensity method sets the intensity of the special effects, and the update method updates the status of the ControlRandomizer instances with a given delta time in seconds.

    """

    def __init__(self, event_manager: OSCEventManager, layer: str):
        self.fx_amount = ControlRandomizer(
            event_manager, layer, "fx_amount", min=0.0, max=1.0
        )
        self.feedback_amount = ControlRandomizer(
            event_manager, layer, "feedback_amount", min=0.0, max=0.33
        )
        self.feedback_fx_amount = ControlRandomizer(
            event_manager, layer, "feedback_fx_amount", min=0.0, max=1.0
        )

    def set_intensity(self, intensity: float):
        self.fx_amount.intensity = intensity
        self.feedback_amount.intensity = intensity
        self.feedback_fx_amount.intensity = intensity

    def update(self, dt: float):
        self.fx_amount.update(dt)
        self.feedback_amount.update(dt)
        self.feedback_fx_amount.update(dt)
