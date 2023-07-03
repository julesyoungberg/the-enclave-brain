# the main app logic
# - initializes everything and handles update logic
#   - set up scene manager, event manager, randomized background
# - takes in control over MIDI
# - sends the data to the simulation
# - determines scene automations via randomized background and one hit cues
# - and then sends out OSC via the event manager

from .controllers.layer_controller import LayerController
from .controllers.lights_controller import LightsController
from .controllers.light_flicker_controller import LightFlickerController
from .controllers.audio_controller import Audio_controller
from .osc.init import INIT_EVENT
from .osc.events import OSCEventManager
from .simulation import Simulation
from . import control

uc_ctrl_idx_to_simulation_key = ['climate_change', 'human_activity', 'fate']

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
        self.light_flicker_controller = LightFlickerController(
            self.event_manager, self.simulation
        )
        self.foley_controller = Audio_controller("foley")
        self.music_controller = Audio_controller("music")
        self.foley_controller.set_scene(self.scene)
        self.music_controller.set_scene(self.scene)
        control.init_uc_comms()


    def update(self, dt: float):
        new_ctrl_data = control.rx_uc_packet()
        received_data = False
        while new_ctrl_data is not None:
            received_data = True
            btn_or_knob, ctrl_idx, ctrl_val = new_ctrl_data
            # print("Received data", btn_or_knob, ctrl_idx, ctrl_val)
            if btn_or_knob == b'p': # for "potentiometer"
                if ctrl_idx < len(uc_ctrl_idx_to_simulation_key):
                    self.simulation.update_config(uc_ctrl_idx_to_simulation_key[ctrl_idx], ctrl_val)
            # elif btn_or_knob is 'b':
                # TODO use ctrl_idx to determine what event is trigged
                # self.simulation.trigger_event()

            new_ctrl_data = control.rx_uc_packet()

        if received_data:
            self.simulation.print_config()

        # update light flicker controller before because it checks if params have changed
        self.light_flicker_controller.update(dt)

        # update simulation - computes scene data and 'commits' params
        self.simulation.update(dt)

        scene_changed = self.scene != self.simulation.scene

        # update controller discrete scene data when needed
        if scene_changed:
            self.scene = self.simulation.scene
            print("\nSCENE CHANGED:", self.scene)
            self.bg_controller.set_scene(self.scene)
            self.fg_controller.set_scene(self.scene)
            self.lights_controller.set_scene(self.scene)
            self.foley_controller.set_scene(self.scene)
            self.music_controller.set_scene(self.scene)

        # print(f"forest_health={self.simulation.forest_health.get_mean()}, scene={self.scene}, scene_intensity={self.simulation.scene_intensity}")
        
        # update controller continuous scene data every frame
        self.bg_controller.set_scene_intensity(self.simulation.scene_intensity)
        self.fg_controller.set_scene_intensity(self.simulation.scene_intensity)
        self.lights_controller.set_scene_intensity(self.simulation.scene_intensity)

        # update controllers
        self.bg_controller.update(dt)
        self.fg_controller.update(dt, force=scene_changed)
        self.lights_controller.update(dt)
        # ambient_audio_controller.update(self.scene, self.simulation)
        self.foley_controller.update(self.scene, self.simulation)
        self.music_controller.update(self.scene, self.simulation)

        # update the event manager last since the controllers may have added events
        self.event_manager.update(dt)
