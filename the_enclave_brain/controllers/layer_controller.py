import random

from .layer_fx_controller import LayerFXController
from ..osc import control_cache
from ..osc.addresses import MADMAPPER_CONFIG, is_one_shot, layer_blackout, control
from ..osc.events import OSCEventManager, OSCEventSequence, OSCEventStack
from ..osc.transitions import LayerSwitch, LayerTransition, TriggerCue, ControlFade
from ..scenes import SCENES


class LayerController:
    """
    Represents a controller for a group of layers that are displayed on a screen.
    This class manages the current state of these layers, including their current scene, layer type, index, and frequency of updates.
    Additionally, the LayerController class handles updating and transitioning between layers based on predefined cues.

    Attributes:
        event_manager (OSCEventManager): The event manager used to manage and send events.
        scene (str): The current scene being displayed.
        current_bin (str): The current bin being displayed.
        layer_type (str): The type of layer being displayed.
        current_layer (str): The current layer being displayed.
        current_index (int): The current index for the layer being displayed.
        time (float): The amount of time that has passed since the last update.
        frequency (float): The frequency at which the layer should be updated.
        prev_scene (str): The previous scene that was displayed.
        cues (list): The list of cues to use for transitioning between layers.
        cue_index (int): The current index of the cue being used for transitioning between layers.
        fx1_controller(LayerFXController): The LayerFXController instance for the first layer.
        fx2_controller(LayerFXController): The LayerFXController instance for the second layer.

    Methods:
        update_layer(): Updates the current layer based on the current scene and cues.
        set_scene(scene: str): Sets the scene to display.
        set_scene_intensity(scene_intensity: float): Sets the intensity of the scene.
        update(dt: float): Updates the layer and its attributes based on a given elapsed time 'dt'.
    """

    def __init__(
        self,
        event_manager: OSCEventManager,
        scene="healthy_forest",
        layer_type="bg",
        frequency=20.0,
    ):
        self.event_manager = event_manager
        self.scene = scene
        self.current_bin = "forest"
        self.layer_type = layer_type
        self.current_layer = None
        self.current_index = 0
        self.time = 0.0
        self.frequency = frequency
        self.prev_scene = None
        self.scene_cues = []
        self.cue_index = 0
        self.fx1_controller = LayerFXController(event_manager, layer_type + "1")
        self.fx2_controller = LayerFXController(event_manager, layer_type + "2")
        self.current_event = None
        self.update_layer()

    def update_layer(self):
        prev_layer = self.current_layer
        prev_bin = self.current_bin
        prev_index = self.current_index
        prev_cue_index = self.cue_index

        # if the scene has changed collect the new scene cues
        if self.scene != self.prev_scene:
            self.prev_scene = self.scene
            self.scene_cues = []
            prev_cue_index = None

            for layer_index in range(2):
                layer_name = self.layer_type + str(layer_index + 1)
                bins = SCENES[self.scene][self.layer_type]
                for bin in bins:
                    if bin not in MADMAPPER_CONFIG[layer_name]["cues"]:
                        continue
                    for cue in range(len(MADMAPPER_CONFIG[layer_name]["cues"][bin])):
                        self.scene_cues.append(
                            {
                                "layer": f"{self.layer_type}{layer_index + 1}",
                                "bin": bin,
                                "cue_index": cue,
                            }
                        )

        if (
            self.current_layer is not None
            and self.layer_type == "fg"
            and "fg_blackout" in SCENES[self.scene]
        ):
            # randomly blackout layer if configured
            if random.random() < SCENES[self.scene]["fg_blackout"]:
                print(f"blacking out {self.layer_type}")
                for i in [1, 2]:
                    layer = f"{self.layer_type}{i}"
                    current_opacity = control_cache.get_value(control(layer, "opacity"))
                    self.current_event = OSCEventSequence(
                        [
                            ControlFade(
                                layer=layer,
                                control="opacity",
                                start=current_opacity,
                                end=0.0,
                                duration=3.0 if current_opacity > 0.0 else 0.0,
                            ),
                            TriggerCue(address=layer_blackout(layer)),
                        ]
                    )
                    self.event_manager.add_event(self.current_event)
                self.current_layer = None
                return

        # choose new cue
        cues = self.cues
        if self.layer_type == "bg":
            other_layer_cues = [cue for cue in self.cues if cue["layer"] != self.current_layer]
            if len(other_layer_cues) > 0:
                cues = other_layer_cues
                prev_cue_index = None
        if prev_cue_index is not None:
            self.cue_index = random.randint(0, len(cues) - 2)
            if self.cue_index >= prev_cue_index:
                self.cue_index += 1
        else:
            self.cue_index = random.randint(0, len(cues) - 1)
        cue = self.scene_cues[self.cue_index]
        self.current_layer = cue["layer"]
        self.current_bin = cue["bin"]
        self.current_index = cue["cue_index"]

        # transition to new cue as needed
        if prev_layer is not None and prev_layer != self.current_layer:
            self.current_event = LayerSwitch(
                prev_layer,
                self.current_layer,
                self.current_bin,
                self.current_index,
                fade=6.0,
                use_mask=self.layer_type == "bg",
                fade_to_black=self.layer_type == "fg" and prev_layer is not None,
            )
            self.event_manager.add_event(self.current_event)
        elif (
            prev_layer is None
            or self.current_bin != prev_bin
            or self.current_index != prev_index
        ):
            self.current_event = LayerTransition(
                self.current_layer,
                self.current_bin,
                self.current_index,
                # @todo consider taking this from the cue config - some foregrounds might not need the fade
                fade=0.0 if self.layer_type == "bg" and prev_layer is not None else 6.0,
            )
            self.event_manager.add_event(self.current_event)

    def set_scene(self, scene: str):
        self.scene = scene

    def set_scene_intensity(self, scene_intensity: float):
        self.fx1_controller.set_intensity(scene_intensity)
        self.fx2_controller.set_intensity(scene_intensity)

    def update(self, dt: float, force=False):
        self.fx1_controller.update(dt)
        self.fx2_controller.update(dt)

        self.time += dt
        if not force and (self.time < self.frequency or not self.current_event.done):
            return

        self.time = 0.0
        self.update_layer()
