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
from .osc.addresses import MADMAPPER_ADDRESSES
from .randomized_background import RandomizedBackground
from .scene import SceneManager
from .simulation import Simulation

TIME_STEP_SECONDS = 1.0 / 60.0

# both BGs have the same bins (unlike FGs)
BG_BINS = list(MADMAPPER_ADDRESSES["bg1"]["cues"].keys())


class App:
    def __init__(self):
        self.simulation = Simulation()
        self.scene_manager = SceneManager()
        self.bg_randomizer = RandomizedBackground()
        self.control_thread = threading.Thread(target=control_loop, args=(self,))
        self.control_thread.start()

    def update(self, dt: float):
        # randomly change bin for now
        if random.uniform(0, 1) < 0.01:
            self.bg_randomizer.bin = BG_BINS[random.randint(0, len(BG_BINS) - 1)]

        self.simulation.update(dt)
        self.scene_manager.step(dt)
        self.bg_randomizer.step(dt)
