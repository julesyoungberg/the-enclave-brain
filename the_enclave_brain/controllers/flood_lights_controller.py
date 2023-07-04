from ..scenes import SCENES
from ..control import tx_floodlight_packet

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
}

class FloodLightsController:
    def __init__(self, scene="healthy_forest"):
        self.scene = scene
        self.scene_changed = True
    
    def set_scene(self, scene: str):
        if scene != self.scene:
            self.scene_changed = True
        self.scene = scene
    
    def update(self, dt: float):
        if not self.scene_changed:
            return

        self.scene_changed = False

        colors = SCENES[self.scene]["flood_lights"]

        for light_idx, color in enumerate(colors):
            r, g, b = PALETTE[color]
            print(f"sending flood light data: idx={light_idx}, r={r}, g={g}, b={b}")
            tx_floodlight_packet(light_idx, r, g, b)

