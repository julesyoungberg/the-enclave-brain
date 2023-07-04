def cue(row: int, col: int, **opts):
    return {"address": f"/cues/selected/cues/by_cell/col_{col}/row_{row}", **opts}


def cues(row: int, count: int, start_column=1, **opts):
    return [cue(row, i + start_column, **opts) for i in range(count)]


def cues_column(col: int, count: int, start_row=1, **opts):
    return [cue(i + start_row, col, **opts) for i in range(count)]


def control_addresses(name: str):
    return {
        "feedback_amount": f"/modules/{name}_FEEDBACK_AMOUNT/Inputs/Input_1",
        "feedback_fx_amount": f"/{name}/feedback/fx_amount",
        "fx_amount": f"/{name}/fx_amount",
        "mask_opacity": f"/surfaces/Layers/{name}_Layers/{name}_Layer_Mask/opacity",
        "opacity": f"/surfaces/Main/{name}/opacity",
    }


MADMAPPER_CONFIG = {
    "fg2": {
        "cues": {
            "birds": cues(4, 2),
            "falling_trees": [cue(19, 1, one_shot=True, clip_length=10)],
            "fires": cues(24, 6),
            "flowers": cues(29, 2),
            "forest": cues(34, 1),
            "mushrooms": cues(42, 1),
            "rain": cues(47, 2),
            "storms": cues(61, 3),
            "winter": cues(69, 1),
            "blackout": cue(74, 4),
            "smoke": cues(55, 4, start_column=11),
        },
        "controls": control_addresses("Foreground_2"),
    },
    "fg1": {
        "cues": {
            "birds": cues(5, 1),
            "falling_tree": [cue(20, 1, one_shot=True, clip_length=10)],
            "fires": cues(25, 2),
            "flowers": cues(30, 2),
            "forest": cues(35, 1),
            "mushrooms": cues(43, 2),
            "storms": cues(62, 3),
            "blackout": cue(74, 3),
            "smoke": cues(56, 3, start_column=11),
        },
        "controls": control_addresses("Foreground_1"),
    },
    "bg2": {
        "cues": {
            "boreal": cues(1, 2),
            "dead": cues(7, 6),
            "deforestation": cues(10, 3),
            "dry_pine": cues(13, 3),
            "fall": cues(16, 5),
            "falling_trees": cues(21, 1),
            "fires": cues(26, 5),
            "flowers": cues(31, 5),
            "forest": cues(36, 2),
            # "mountains": cues(39, 2),
            "mushrooms": cues(44, 2),
            "rain": cues(49, 3),
            "rainforest": cues(52, 6),
            "smoke": cues(55, 1),
            "spring": cues(58, 4),
            "storms": cues(63, 3),
            "summer": cues(66, 6),
            "winter": cues(71, 5),
            "blackout": cue(74, 2),
            "drought": cues(78, 2),
            "industry": cues(83, 3),
            "pollution": cues(88, 1),
            "roads": cues(93, 2),
            "growth": cues(98, 4),
            "logging": cues(103, 1),
        },
        "controls": control_addresses("Background_2"),
    },
    "bg1": {
        "cues": {
            "boreal": cues(2, 1),
            "dead": cues(8, 6),
            "deforestation": cues(11, 2),
            # "dry_pine": cues(14, 2),
            "fall": cues(17, 4),
            "falling_trees": cues(22, 1),
            "fires": cues(27, 5),
            "flowers": cues(32, 2),
            "forest": cues(37, 3),
            # "mountains": cues(40, 2),
            "mushrooms": cues(45, 2),
            "rain": cues(50, 4),
            "rainforest": cues(53, 5),
            "smoke": cues(56, 3),
            "spring": cues(59, 4),
            "storms": cues(64, 1),
            "summer": cues(67, 6),
            "winter": cues(72, 6),
            "blackout": cue(74, 1),
            "drought": cues(79, 2),
            "industry": cues(84, 2),
            "pollution": cues(89, 1),
            "roads": cues(94, 3),
            "growth": cues(99, 5),
            "logging": cues(104, 4),
        },
        "controls": control_addresses("Background_1"),
    },
    "lights": {
        "content": cues(1, 4, start_column=11),
        "colors": {
            "healthy_forest": cues_column(11, 3, start_row=2),
            "burning_forest": cues_column(12, 3, start_row=2),
            "dead_forest": cues_column(13, 3, start_row=2),
            "growing_forest": cues_column(11, 3, start_row=2), # @todo find different colors
            "climate_change": cues_column(14, 3, start_row=2),
            "deforestation": cues_column(15, 3, start_row=2),
            "rain": cues_column(16, 3, start_row=2),
            "storm": cues_column(17, 3, start_row=2),
        },
        "controls": {
            "tubes1_brightness": "/modules/TUBES_1_BRIGHTNESS/Inputs/Input_1",
            "tubes2_brightness": "/modules/TUBES_2_BRIGHTNESS/Inputs/Input_1",
            "tubes3_brightness": "/modules/TUBES_3_BRIGHTNESS/Inputs/Input_1",
            "lanterns1_brightness": "/modules/LANTERNS_1_BRIGHTNESS/Inputs/Input_1",
            "lanterns2_brightness": "/modules/LANTERNS_2_BRIGHTNESS/Inputs/Input_1",
            "speed": "/Lights/Speed",
        },
    },
}


def lights_control_address(light_control: str) -> str:
    return MADMAPPER_CONFIG["lights"]["controls"][light_control]

def lights_content_address(content_index: int):
    return MADMAPPER_CONFIG["lights"]["content"][content_index]["address"]

def lights_color_address(scene: str, color_index: int) -> str:
    return MADMAPPER_CONFIG["lights"]["colors"][scene][color_index]["address"]

def layer_blackout(layer: str) -> str:
    return MADMAPPER_CONFIG[layer]["cues"]["blackout"]["address"]


def layer_cue(layer: str, bin: str, index: int) -> dict:
    return MADMAPPER_CONFIG[layer]["cues"][bin][index]


def layer_cue_address(layer: str, bin: str, index: int) -> str:
    return layer_cue(layer, bin, index)["address"]


def control(layer: str, control: str) -> str:
    return MADMAPPER_CONFIG[layer]["controls"][control]


def is_one_shot(layer: str, bin: str, index: int) -> bool:
    config = layer_cue(layer, bin, index)
    return "one_shot" in config and config["one_shot"]


def clip_length(layer: str, bin: str, index: int) -> float:
    config = layer_cue(layer, bin, index)
    if "clip_length" in config:
        return config["clip_length"]
    return 6.0
