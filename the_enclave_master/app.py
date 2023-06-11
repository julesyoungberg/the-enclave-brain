# the main app logic
# - initializes everything and handles update logic
#   - set up scene manager, event manager, randomized background
# - takes in control over MIDI
# - sends the data to the simulation
# - determines scene automations via randomized background and one hit cues
# - and then sends out OSC via the event manager

import random
import threading

from .control import control_loop
from .layer_randomizer import LayerRandomizer
from .osc.events import OSCEventManager
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
        self.event_manager = OSCEventManager()
        self.scene = 0
        self.bg_randomizer = LayerRandomizer(
            self.event_manager, layer_type="bg", scene=SCENE_NAMES[self.scene]
        )
        self.fg_randomizer = LayerRandomizer(
            self.event_manager, layer_type="fg", scene=SCENE_NAMES[self.scene]
        )
        self.control_thread = threading.Thread(target=control_loop, args=(self,))
        self.control_thread.start()

    def update(self, dt: float):
        # randomly change scene for now
        if random.uniform(0, 1) < 0.00005:
            self.scene = (self.scene + 1) % len(SCENE_NAMES)
            # @todo implement slow transition where fg changes first for 30 seconds or so
            new_scene = SCENE_NAMES[self.scene]
            self.bg_randomizer.scene = new_scene
            self.fg_randomizer.scene = new_scene

        self.simulation.update(dt)
        self.event_manager.update(dt)
        self.bg_randomizer.update(dt)
        self.fg_randomizer.update(dt)
