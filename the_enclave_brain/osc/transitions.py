import datetime

from . import addresses
from . import control_cache
from .events import OSCEvent, OSCSleepEvent, OSCEventSequence, OSCEventStack


class OSCTransition(OSCEvent):
    """Represents the transition of an OSC message's parameter value over time.

    Attributes:
        start (float): The start value of the parameter.
        end (float): The end value of the parameter.
    """

    def __init__(
        self, address: str, start: float, end: float, duration: float, debug=False
    ):
        super().__init__(address, duration, debug=debug)
        self.start = start
        self.end = end

    def update(self, dt: float):
        """Calculates the current parameter value based on time and sends an OSC message with the current value to the specified address.

        Args:
            dt (float): The time elapsed since the last call to step.
        """
        value = self.end
        if self.duration > 0.0:
            value = (self.time / self.duration) * (self.end - self.start) + self.start
        control_cache.set_value(self.address, value)
        super().update(dt, value)


class ControlFade(OSCTransition):
    """Represents a control transition for a layer."""

    def __init__(
        self,
        layer: str,
        control: str,
        start: float,
        end: float,
        duration: float,
        debug=False,
    ):
        # if control == "opacity":
        #     print(
        #         f"ControlFade: layer={layer}, control={control}, start={start}, end={end}, duration={duration}"
        #     )
        address = addresses.control(layer, control)
        super().__init__(address, start, end, duration, debug=debug)


class LayerTransition(OSCEventSequence):
    """A class that defines a sequence of events for transitioning a layer in a media player.
    The class inherits from OSCEventSequence.

    Attributes:
    - layer (str): The name of the layer to transition.
    - cue_bin (str): The name of the cue bank associated with the layer.
    - cue_index (int): The index of the cue to trigger.
    - use_mask (bool): Determines whether or not the transition should use a mask.
    - fade (float): The duration of the fade, in seconds, if any.
    """

    def __init__(
        self,
        layer: str,
        cue_bin: str,
        cue_index: int,
        use_mask=False,
        fade=0.0,
    ):
        # print(
        #     f"\nLayerTransition: layer={layer}, cue_bin={cue_bin}, cue_index={cue_index}, fade={fade}, use_mask={use_mask}"
        # )
        events = []

        is_one_shot = addresses.is_one_shot(layer, cue_bin, cue_index)

        current_opacity = control_cache.get_value(addresses.control(layer, "opacity"))
        mask_opacity = control_cache.get_value(addresses.control(layer, "mask_opacity"))

        if fade > 0.0 and current_opacity > 0.0:
            if use_mask:
                if mask_opacity < 1.0:
                    events.append(
                        ControlFade(layer, "mask_opacity", mask_opacity, 1.0, fade)
                    )
            else:
                events.append(ControlFade(layer, "opacity", current_opacity, 0.0, fade))

        if is_one_shot:
            events.append(PlayOneShot(layer, cue_bin, cue_index))
        else:
            events.append(
                TriggerCue(
                    layer,
                    cue_bin,
                    cue_index,
                )
            )

            events.append(OSCSleepEvent(6.0))

            if fade > 0:
                if use_mask:
                    events.append(ControlFade(layer, "mask_opacity", 1.0, 0.5, fade))
                else:
                    events.append(ControlFade(layer, "opacity", 0.0, 1.0, fade))
            elif current_opacity < 1.0:
                events.append(ControlFade(layer, "opacity", current_opacity, 1.0, fade))

        super().__init__(events)


class LayerSwitch(OSCEventSequence):
    """
    A class that represents a layer switch event sequence.

    Args:
        prev_layer (str): The name of the previous layer to be switched.
        next_layer (str): The name of the next layer to be switched.
        cue_bin (int): The number of the cue to be triggered in the next layer.
        cue_index (int): The index of the cue to be triggered in the next layer.
        fade (float): The fade duration for all fade effects in the sequence.
        use_mask (bool): A flag indicating whether a mask should be used or not.
    """

    def __init__(
        self,
        prev_layer: str,
        next_layer: str,
        cue_bin: str,
        cue_index: int,
        fade=6.0,
        use_mask=False,
        fade_to_black=False,
    ):
        # print(
        #     f"\nLayerSwitch: prev_layer={prev_layer}, next_layer={next_layer}, cue_bin={cue_bin}, cue_index={cue_index}, fade={fade}, use_mask={use_mask}"
        # )
        events = []

        swap_events = []

        prev_layer_opacity = control_cache.get_value(
            addresses.control(prev_layer, "opacity")
        )
        prev_layer_mask_opacity = control_cache.get_value(
            addresses.control(prev_layer, "mask_opacity")
        )
        next_layer_opacity = control_cache.get_value(
            addresses.control(next_layer, "opacity")
        )
        next_layer_mask_opacity = control_cache.get_value(
            addresses.control(next_layer, "mask_opacity")
        )

        if prev_layer_opacity > 0.5:
            swap_events.append(
                ControlFade(prev_layer, "opacity", prev_layer_opacity, 0.5, fade)
            )
            prev_layer_opacity = 0.5

        is_one_shot = addresses.is_one_shot(next_layer, cue_bin, cue_index)

        if not is_one_shot:
            events.append(TriggerCue(next_layer, cue_bin, cue_index))
            events.append(OSCSleepEvent(6.0))
            if use_mask and next_layer_mask_opacity < 1.0:
                events.append(
                    ControlFade(
                        next_layer,
                        "mask_opacity",
                        next_layer_mask_opacity,
                        1.0,
                        3.0 if next_layer_opacity > 0.0 else 0.0,
                    )
                )
                next_layer_mask_opacity = 1.0

            if fade_to_black and next_layer_opacity < 0.5:
                events.append(
                    ControlFade(next_layer, "opacity", next_layer_opacity, 0.5, fade)
                )
                next_layer_opacity = 0.5

            swap_events.append(
                ControlFade(next_layer, "opacity", next_layer_opacity, 1.0, fade)
            )

            if use_mask:
                if prev_layer_mask_opacity < 1.0:
                    swap_events.append(
                        ControlFade(
                            prev_layer, "mask_opacity", prev_layer_opacity, 1.0, fade
                        )
                    )
                if next_layer_mask_opacity > 0.5:
                    swap_events.append(
                        ControlFade(
                            next_layer,
                            "mask_opacity",
                            next_layer_mask_opacity,
                            0.5,
                            fade,
                        )
                    )

        if len(swap_events) > 0:
            events.append(OSCEventStack(swap_events))

        if prev_layer_opacity > 0.0 and fade_to_black:
            events.append(
                ControlFade(prev_layer, "opacity", prev_layer_opacity, 0.0, fade)
            )

        if is_one_shot:
            events.append(PlayOneShot(next_layer, cue_bin, cue_index))

        super().__init__(events)


class TriggerCue(OSCEvent):
    """Represents an instantaneous OSC that triggers a cue for a specific layer, cue bank, and index."""

    def __init__(self, layer=None, cue_bin=None, cue_index=None, address=None):
        # print(
        #     f"TriggerCue: layer={layer}, cue_bin={cue_bin}, cue_index={cue_index}, address={address}"
        # )
        if (layer == None or cue_bin == None or cue_index == None) and address == None:
            raise Exception(
                "Invalid cue config, must provide an address, or the layer, bin, and index"
            )
        if address is None:
            address = addresses.layer_cue_address(layer, cue_bin, cue_index)
        super().__init__(address)

    def update(self, dt: float):
        super().update(dt, 1.0)


class PlayOneShot(OSCEventSequence):
    """
    A class that represents a sequence of events to play a one-shot video cue in a given MadMapper layer.

    Attributes:
    - layer (str): The name of the layer in which the cue is being played.
    - cue_bin (str): The name of the cue bin containing the cue.
    - cue_index (int): The index of the cue within the cue bin.
    - fade (float): The duration (in seconds) of the fade-out when the cue ends. Defaults to 1.0.

    Methods:
    - __init__(self, layer, cue_bin, cue_index, fade=1.0): The constructor method that initializes the event sequence with
    a list of events, including a blackout trigger before the cue starts, a fade-in, and a fade-out on movie end (if fade > 0).
    """

    def __init__(self, layer: str, cue_bin: str, cue_index: int, fade=1.0):
        # print(
        #     f"PlayOneShot: layer={layer}, cue_bin={cue_bin}, cue_index={cue_index}, fade={fade}"
        # )
        events = []

        # make sure the layer is blank (blackout)
        events.append(TriggerCue(address=addresses.layer_blackout(layer)))

        events.append(OSCSleepEvent(1.0))

        # set the opacity
        events.append(ControlFade(layer, "opacity", 0.0, 1.0, 0.0))

        # play the cue
        events.append(
            TriggerCue(
                layer,
                cue_bin,
                cue_index,
            )
        )

        # sleep till movie end
        events.append(OSCSleepEvent(addresses.clip_length(layer, cue_bin, cue_index)))

        # fade out on movie end
        events.append(ControlFade(layer, "opacity", 1.0, 0.0, fade))

        super().__init__(events)


class OSCFlicker(OSCEventSequence):
    """
    A class representing an OSC flicker event sequence.
    Inherits from the OSCEventSequence base class.

    Args:
        address (str): The OSC address to send the flicker event to.
        high (float): The initial value of the address.
        low (float): The final value of the address.
        period (float): The period of each flicker cycle.
        n_flicks (int): The number of flicker cycles to repeat.
        debug (bool): Indicates whether debug messages should be printed in the console.
        
    Attributes:
        events (list): A list of OSCTransition objects representing the flicker events.
    """

    def __init__(
        self, address: str, high=1.0, low=0.0, period=1.0, n_flicks=1, debug=False
    ):
        # print(
        #     f"OSCFlicker address={address}, high={high}, low={low}, period={period}, n_flicks={n_flicks}"
        # )
        events = []

        for _ in range(n_flicks):
            events.append(OSCTransition(address, high, low, period / 2.0, debug=debug))
            events.append(OSCTransition(address, low, high, period / 2.0, debug=debug))
        
        super().__init__(events)
