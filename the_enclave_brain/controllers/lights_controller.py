import math
import random

from ..osc import control_cache
from ..osc.addresses import MADMAPPER_CONFIG, lights_color_address, lights_content_address, lights_control_address
from ..osc.events import OSCEventManager
from ..osc.transitions import TriggerCue, OSCTransition


class LightsController:
    """
    A controller for triggering lighting and color cues based on scene intensity and frequency.

    Args:
        event_manager (OSCEventManager): An instance of the OSCEventManager class for managing OSC events.
        scene (str): The current scene for controlling the lights (default: "healthy_forest").
        frequency (float): The frequency of update in seconds (default: 20.0).

    Attributes:
        event_manager (OSCEventManager): An instance of the OSCEventManager class for managing OSC events.
        scene (str): The current scene for controlling the lights.
        frequency (float): The frequency of update in seconds.
        scene_intensity (float): The intensity of the scene.
        time (float): The elapsed time since the last update.
        current_content_index (int): The index of the current content based on scene intensity.
        prev_scene (str): The previous scene.

    Methods:
        set_scene(scene: str): Sets the current scene for controlling the lights.
        set_scene_intensity(scene_intensity: float): Sets the intensity of the current scene.
        update(dt: float): Updates the lighting and color cues based on scene intensity and frequency.
    """

    def __init__(
        self, event_manager: OSCEventManager, scene="healthy_forest", frequency=20.0
    ):
        self.event_manager = event_manager
        self.scene = scene
        self.frequency = frequency
        self.scene_intensity = 0.0
        self.time = 0.0
        self.current_content_index = 0
        self.prev_scene = None

    def set_scene(self, scene: str):
        self.scene = scene

    def set_scene_intensity(self, scene_intensity: float):
        self.scene_intensity = scene_intensity

    def update(self, dt: float):
        # update light speed according to the scene intensity
        speed_address = lights_control_address("speed")
        target_speed = self.scene_intensity
        self.event_manager.add_event(
            OSCTransition(address=speed_address, start=0.0, end=target_speed, duration=0.0)
        )

        content_index = round(
            self.scene_intensity * (len(MADMAPPER_CONFIG["lights"]["content"]) - 1)
        )

        # update the content according to the scene intensity
        if content_index != self.current_content_index:
            print("updating lights content")
            self.current_content_index = content_index
            self.event_manager.add_event(
                TriggerCue(
                    address=lights_content_address(self.current_content_index)
                )
            )

        scene_changed = self.scene != self.prev_scene
        self.prev_scene = self.scene
        self.time += dt

        if not scene_changed and self.time < self.frequency:
            return

        self.time = 0.0

        color_index = random.randint(
            1, len(MADMAPPER_CONFIG["lights"]["colors"][self.scene]) - 1
        )

        print("updating lights color")
        self.event_manager.add_event(
            TriggerCue(
                address=lights_color_address(self.scene, color_index)
            )
        )
