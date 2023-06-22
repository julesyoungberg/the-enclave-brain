from . import addresses
from .transitions import OSCEventStack, TriggerCue, ControlFade

# initial reset - black out every layer and reset fx and masks
MADMAPPER_RESET_EVENT = OSCEventStack(
    [
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
    ]
)
