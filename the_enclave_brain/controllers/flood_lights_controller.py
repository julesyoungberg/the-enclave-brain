from ..scenes import SCENES
from ..control import tx_floodlight_packet
from .light_fade_controller import LightFadeController

PALETTE = {
    "green": (0, 122, 10),
    "blue": (0, 15, 128),
    "red": (128, 0, 0),
    "orange": (179, 0, 0),
    "brown": (125, 79, 0),
    "grey": (130, 130, 130),
    "orange": (191, 120, 0),
    "teal": (0, 125, 89),
    "indigo": (33, 0, 125),
    "purple": (112, 0, 125),
    "black": (0, 0, 0),
}

def get_scene_colors(scene: str):
    return [PALETTE[color] for color in SCENES[scene]["flood_lights"]]

class FloodLightsController:
    def __init__(self, scene="healthy_forest"):
        self.scene = scene
        self.transitions = []
        self.current_colors = get_scene_colors(scene)
        self.send_colors()

    def send_colors(self):
        for light_idx, color in enumerate(self.current_colors):
            r, g, b = color
            print(f"sending flood light data: idx={light_idx}, r={r}, g={g}, b={b}")
            tx_floodlight_packet(light_idx, r, g, b)
    
    def set_scene(self, scene: str):
        if scene == self.scene:
            return

        next_colors = get_scene_colors(scene)
        self.transitions = [
            LightFadeController(
                self.current_colors[0],
                next_colors[0]
            ),
            LightFadeController(
                self.current_colors[1],
                next_colors[1]
            ),
        ]
        self.scene = scene
    
    def update(self, dt: float):
        if len(self.transitions) == 0:
            return
        
        self.transitions[0].update(dt)
        self.transitions[1].update(dt)

        self.current_colors = [
            self.transitions[0].get_current_color(),
            self.transitions[1].get_current_color(),
        ]
        self.send_colors()

        if self.transitions[0].done and self.transitions[1].done:
            self.transitions = []

