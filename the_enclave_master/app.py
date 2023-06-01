# the main app logic
# - initializes everything and handles update logic
#   - set up scene manager, event manager, randomized background
# - takes in control over MIDI
# - sends the data to the simulation
# - determines scene automations via randomized background and one hit cues
# - and then sends out OSC via the event manager

import threading

from .control import control_loop
from .scene import SceneManager
from .randomized_background import RandomizedBackground
from .simulation import Simulation

TIME_STEP_SECONDS = 1.0 / 60.0


class App:
    def __init__(self):
        self.simulation = Simulation()
        self.scene_manager = SceneManager()
        self.bg_randomizer = RandomizedBackground()
        self.control_thread = threading.Thread(target=control_loop, args=(self,))
        self.control_thread.start()

    def update(self, dt: float):
        self.simulation.update(dt)
        self.scene_manager.step(dt)
        self.bg_randomizer.step(dt)
