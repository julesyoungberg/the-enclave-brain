import random

from .layer_fx_control import LayerFXControl
from .osc.addresses import MADMAPPER_CONFIG, is_one_shot
from .osc.events import OSCEventManager
from .osc.transitions import LayerSwitch, LayerTransition
from .scenes import SCENES


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
        cue_idx (int): The current index of the cue being used for transitioning between layers.
        fx1_control (LayerFXControl): The LayerFXControl instance for the first layer.
        fx2_control (LayerFXControl): The LayerFXControl instance for the second layer.

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
        frequency=30.0,
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
        self.cues = []
        self.cue_idx = 0
        self.fx1_control = LayerFXControl(event_manager, layer_type + "1")
        self.fx2_control = LayerFXControl(event_manager, layer_type + "2")

    def update_layer(self):
        # randomly select new layer and cue
        was_one_shot = False
        if self.current_layer is not None:
            was_one_shot = is_one_shot(
                self.current_layer, self.current_bin, self.current_index
            )

        prev_layer = self.current_layer
        prev_bin = self.current_bin
        prev_index = self.current_index

        if self.scene != self.prev_scene:
            self.prev_scene = self.scene
            self.cues = []

            for layer_index in range(2):
                layer_name = self.layer_type + str(layer_index + 1)
                bins = SCENES[self.scene][self.layer_type]
                for bin in bins:
                    if bin not in MADMAPPER_CONFIG[layer_name]["cues"]:
                        continue
                    for cue in MADMAPPER_CONFIG[layer_name]["cues"][bin]:
                        self.cues.append(
                            {
                                "layer_index": layer_index + 1,
                                "bin": bin,
                                "cue": cue,
                            }
                        )

        self.cue_idx = random.randint(0, len(self.cues) - 1)
        cue = self.cues[self.cue_idx]
        layer_index = cue["layer_index"]
        self.current_layer = f"{self.layer_type}{layer_index}"
        self.current_bin = cue["bin"]
        self.current_indx = cue["cue"]

        if prev_layer is not None and prev_layer != self.current_layer:
            self.event_manager.add_event(
                LayerSwitch(
                    prev_layer,
                    self.current_layer,
                    self.current_bin,
                    self.current_index,
                    fade=6.0,
                    use_mask=self.layer_type == "bg",
                    prev_was_one_shot=was_one_shot,
                )
            )
        elif (
            prev_layer is None
            or self.current_bin != prev_bin
            or self.current_index != prev_index
        ):
            self.event_manager.add_event(
                LayerTransition(
                    self.current_layer,
                    self.current_bin,
                    self.current_index,
                    # @todo consider taking this from the cue config - some foregrounds might not need the fade
                    fade=0.0
                    if self.layer_type == "bg" and prev_layer is not None
                    else 6.0,
                    prev_was_one_shot=was_one_shot,
                )
            )

    def set_scene(self, scene: str):
        self.scene = scene

    def set_scene_intensity(self, scene_intensity: float):
        self.fx1_control.set_intensity(scene_intensity)
        self.fx2_control.set_intensity(scene_intensity)

    def update(self, dt: float):
        self.fx1_control.update(dt)
        self.fx2_control.update(dt)

        self.time += dt
        if self.time < self.frequency:
            return

        self.time = 0.0
        self.update_layer()
