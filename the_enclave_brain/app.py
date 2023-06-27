# the main app logic
# - initializes everything and handles update logic
#   - set up scene manager, event manager, randomized background
# - takes in control over MIDI
# - sends the data to the simulation
# - determines scene automations via randomized background and one hit cues
# - and then sends out OSC via the event manager

import threading

from .control import control_loop
from .controllers.layer_controller import LayerController
from .controllers.lights_controller import LightsController
from .osc.init import INIT_EVENT
from .osc.events import OSCEventManager
from .simulation import Simulation

TIME_STEP_SECONDS = 1.0 / 60.0


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
        self.event_manager.add_event(INIT_EVENT)

        # set initial scene and create layer randomizers
        self.scene = self.simulation.scene
        self.bg_controller = LayerController(
            self.event_manager, layer_type="bg", scene=self.scene
        )
        self.fg_controller = LayerController(
            self.event_manager, layer_type="fg", scene=self.scene
        )
        self.lights_controller = LightsController(
            self.event_manager, scene=self.scene
        )

    def update(self, dt: float):
        # update scene first and pass scene data to controllers
        self.simulation.update(dt)
        scene_changed = self.scene != self.simulation.scene
        if scene_changed:
            self.scene = self.simulation.scene
            self.bg_controller.set_scene(self.simulation.scene)
            self.fg_controller.set_scene(self.simulation.scene)
            self.lights_controller.set_scene(self.simulation.scene)
        self.bg_controller.set_scene_intensity(self.simulation.scene_intensity)
        self.fg_controller.set_scene_intensity(self.simulation.scene_intensity)
        self.lights_controller.set_scene_intensity(self.simulation.scene_intensity)

        # update controllers
        self.bg_controller.update(dt)
        self.fg_controller.update(dt, force=scene_changed)
        self.lights_controller.update(dt)

        # update the event manager last since the controllers may have added events
        self.event_manager.update(dt)
