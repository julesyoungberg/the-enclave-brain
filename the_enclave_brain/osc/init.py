from . import addresses
from ..config import MAX_LIGHT_BRIGHTNESS
from .transitions import OSCEventStack, TriggerCue, OSCTransition, ControlFade

# initial reset - black out every layer and reset fx and masks
INIT_EVENT = OSCEventStack(
    [
        *[
            OSCEventStack(
                [
                    TriggerCue(address=addresses.layer_blackout(layer)),
                    *[
                        ControlFade(
                            layer=layer,
                            control=control,
                            start=0.0,
                            end=0.0,
                            duration=0.0,
                        )
                        for control in [
                            "feedback_amount",
                            "feedback_fx_amount",
                            "fx_amount",
                            "mask_opacity",
                            "opacity",
                        ]
                    ],
                ]
            )
            for layer in ["bg1", "bg2", "fg1", "fg2"]
        ],
        *[
            OSCTransition(address=addresses.lights_control_address(control), start=0.0, end=MAX_LIGHT_BRIGHTNESS, duration=6.0)
            for control in addresses.MADMAPPER_CONFIG["lights"]["controls"].keys()
        ],
    ]
)
