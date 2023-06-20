# the main app logic
# - initializes everything and handles update logic
#   - set up scene manager, event manager, randomized background
# - takes in control over MIDI
# - sends the data to the simulation
# - determines scene automations via randomized background and one hit cues
# - and then sends out OSC via the event manager

import threading

from .control import control_loop
from .layer_fx_control import LayerFXControl
from .layer_controller import LayerController
from .osc import addresses
from .osc.events import OSCEventManager
from .osc.transitions import OSCEventStack, TriggerCue, ControlFade
from .scenes import SCENES
from .simulation import Simulation

TIME_STEP_SECONDS = 1.0 / 60.0

SCENE_NAMES = list(SCENES.keys())


class App:
    """
    Represents the main application class of the program.
    This class is responsible for managing the simulation, initiating the control thread and updating the layer controller's state.

    Attributes:
        simulation (Simulation): Instance of the simulation class used to simulate different states.
        control_thread (threading.Thread): Thread instance used to run the control loop function.
        event_manager (OSCEventManager): The event manager used to manage and send events.
        bg_controller (LayerController): Instance of LayerController class representing the background layer.
        fg_controller (LayerController): Instance of LayerController class representing the foreground layer.

    Methods:
        update(dt: float): Updates the simulation, sets the scene and scene intensity for the background and foreground layer controller and updates all controllers with elapsed time 'dt'.
    """

    def __init__(self):
        self.simulation = Simulation()
        self.control_thread = threading.Thread(target=control_loop, args=(self,))
        self.control_thread.start()

        self.event_manager = OSCEventManager()

        # initial reset - black out every layer and reset fx and masks
        self.event_manager.add_event(
            OSCEventStack(
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
        )

        # set initial scene and create layer randomizers
        scene = SCENE_NAMES[0]
        self.bg_controller = LayerController(
            self.event_manager, layer_type="bg", scene=scene
        )
        self.fg_controller = LayerController(
            self.event_manager,
            layer_type="fg",
            scene=scene,
            frequency=30.0,
        )

    def update(self, dt: float):
        self.simulation.update(dt)

        # @todo try updating foreground a few or many seconds before bg?
        # alternatively could separate foreground and background scenes for events
        # foreground scenes for forest, rain, and fire could be scene as "light" versions
        self.bg_controller.set_scene(self.simulation.scene)
        self.fg_controller.set_scene(self.simulation.scene)
        self.bg_controller.set_scene_intensity(0.9)
        self.fg_controller.set_scene_intensity(0.9)

        self.event_manager.update(dt)
        self.bg_controller.update(dt)
        self.fg_controller.update(dt)
