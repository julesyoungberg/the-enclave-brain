def cue(row: int, col: int, **opts):
    return {"address": f"/cues/selected/cues/by_cell/col_{col}/row_{row}", **opts}


def cues(row: int, count: int, **opts):
    return [cue(row, i + 1, **opts) for i in range(count)]


def control_addresses(name: str):
    return {
        "feedback_amount": f"/surfaces/Layers/{name}_Layers/{name}_Layer_Feedback/opacity",
        "feedback_fx_amount": f"/{name}/feedback/fx_amount",
        "fx_amount": f"/{name}/fx_amount",
        "mask_opacity": f"/surfaces/Layers/{name}_Layers/{name}_Layer_Mask/opacity",
        "opacity": f"/surfaces/Main/{name}/opacity",
    }


MADMAPPER_CONFIG = {
    "fg2": {
        "cues": {
            "birds": cues(4, 4),
            "falling_trees": [cue(19, 1, one_shot=True, clip_length=10)],
            "fires": cues(24, 8),
            "flowers": cues(29, 1),
            "forest": cues(34, 1),
            "mushrooms": cues(42, 1),
            "rain": cues(47, 2),
            "storms": cues(61, 3),
            "winter": cues(69, 1),
            "blackout": cue(74, 4),
        },
        "controls": control_addresses("Foreground_2"),
    },
    "fg1": {
        "cues": {
            "birds": cues(5, 1),
            "falling_tree": [cue(20, 1, one_shot=True, clip_length=10)],
            "fires": cues(25, 2),
            "flowers": cues(30, 3),
            "forest": cues(35, 1),
            "mushrooms": cues(43, 2),
            "storms": cues(62, 3),
            "blackout": cue(74, 3),
        },
        "controls": control_addresses("Foreground_1"),
    },
    "bg2": {
        "cues": {
            "boreal": cues(1, 2),
            "dead": cues(7, 3),
            "deforestation": cues(10, 6),
            "dry_pine": cues(13, 4),
            "fall": cues(16, 5),
            "falling_trees": cues(21, 1),
            "fires": cues(26, 10),
            "flowers": cues(31, 5),
            "forest": cues(36, 2),
            "mountains": cues(39, 3),
            "mushrooms": cues(44, 2),
            "rain": cues(49, 6),
            "rainforest": cues(52, 6),
            "smoke": cues(55, 7),
            "spring": cues(58, 4),
            "storms": cues(63, 3),
            "summer": cues(66, 6),
            "winter": cues(71, 5),
            "blackout": cue(74, 2),
            "drought": cues(78, 1),
            "industry": cues(83, 2),
            "pollution": cues(88, 3),
            "roads": cues(93, 2),
        },
        "controls": control_addresses("Background_2"),
    },
    "bg1": {
        "cues": {
            "boreal": cues(2, 1),
            "dead": cues(8, 5),
            "deforestation": cues(11, 7),
            "dry_pine": cues(14, 2),
            "fall": cues(17, 4),
            "falling_trees": cues(22, 1),
            "fires": cues(27, 9),
            "flowers": cues(32, 2),
            "forest": cues(37, 3),
            # "mountains": cues(40, 2),
            "mushrooms": cues(45, 2),
            "rain": cues(50, 6),
            "rainforest": cues(53, 5),
            "smoke": cues(56, 6),
            "spring": cues(59, 4),
            "storms": cues(64, 2),
            "summer": cues(67, 6),
            "winter": cues(72, 6),
            "blackout": cue(74, 1),
            "drought": cues(79, 1),
            "industry": cues(84, 2),
            "pollution": cues(89, 2),
            "roads": cues(94, 2),
        },
        "controls": control_addresses("Background_1"),
    },
    "lights": {},
}


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
