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
from .layer_randomizer import LayerRandomizer
from .osc import addresses
from .osc.events import OSCEventManager
from .osc.transitions import OSCEventStack, TriggerCue
from .scenes import SCENES
from .simulation import Simulation

TIME_STEP_SECONDS = 1.0 / 60.0

SCENE_NAMES = list(SCENES.keys())


class App:
    """
    Main application class for running simulation and managing visual layer updates.

    Attributes:
        simulation (Simulation): The simulation instance used for updating the physics simulation.
        event_manager (OSCEventManager): The event manager instance used for managing OSC events.
        bg_randomizer (LayerRandomizer): The layer randomizer instance used for updating the background layer.
        fg_randomizer (LayerRandomizer): The layer randomizer instance used for updating the foreground layer.
        control_thread (Thread): The control thread instance used for running the control loop.

    Methods:
        update(dt): Updates the simulation and visual layers, including randomly changing the scene.

    """

    def __init__(self):
        self.simulation = Simulation()
        self.control_thread = threading.Thread(target=control_loop, args=(self,))
        self.control_thread.start()

        self.event_manager = OSCEventManager()
        # black out every layer
        self.event_manager.add_event(
            OSCEventStack(
                [
                    TriggerCue(address=addresses.layer_blackout(layer))
                    for layer in ["bg1", "bg2", "fg1", "fg2"]
                ]
            )
        )

        # set initial scene and create layer randomizers
        self.scene = 0
        self.bg_randomizer = LayerRandomizer(
            self.event_manager, layer_type="bg", scene=SCENE_NAMES[self.scene]
        )
        self.fg_randomizer = LayerRandomizer(
            self.event_manager, layer_type="fg", scene=SCENE_NAMES[self.scene]
        )
        self.bg1_fx = LayerFXControl(self.event_manager, "bg1")
        self.bg2_fx = LayerFXControl(self.event_manager, "bg2")
        self.fg1_fx = LayerFXControl(self.event_manager, "fx1")
        self.fg2_fx = LayerFXControl(self.event_manager, "fx2")

    def update(self, dt: float):
        self.simulation.update(dt)
        self.bg_randomizer.scene = self.simulation.scene
        self.fg_randomizer.scene = self.simulation.scene
        self.bg1_fx.set_intensity(self.simulation.scene_intensity)
        self.bg2_fx.set_intensity(self.simulation.scene_intensity)
        self.fg1_fx.set_intensity(self.simulation.scene_intensity)
        self.fg2_fx.set_intensity(self.simulation.scene_intensity)

        self.event_manager.update(dt)
        self.bg_randomizer.update(dt)
        self.fg_randomizer.update(dt)
        self.bg1_fx.update(dt)
        self.bg2_fx.update(dt)
        self.fg1_fx.update(dt)
        self.fg2_fx.update(dt)
