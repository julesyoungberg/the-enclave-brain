def cues(row: int, count: int):
    return [f"/cues/selected/cues/by_cell/col_{i + 1}/row_{row}" for i in range(count)]


def control_addresses(name: str):
    return {
        "feedback_amount": f"/surfaces/Layers/{name}_Layers/{name}_Layer_Feedback/opacity",
        "feedback_fx_amount": f"/{name}/feedback/fx_amount",
        "fx_amount": f"/{name}/fx_amount",
        "mask_opacity": f"/surfaces/Layers/{name}_Layers/{name}_Layer_Mask/opacity",
        "opacity": f"/surfaces/Main/{name}/opacity",
    }


MADMAPPER_ADDRESSES = {
    "fg2": {
        "cues": {
            "birds": cues(4, 4),
            "falling_trees": cues(19, 1),
            "fires": cues(24, 8),
            "flowers": cues(29, 4),
            "forest": cues(34, 1),
            "mushrooms": cues(42, 5),
            "rain": cues(47, 2),
            "storms": cues(61, 3),
            "winter": cues(69, 1),
        },
        "controls": control_addresses("Foreground_2"),
    },
    "fg1": {
        "cues": {
            "birds": cues(5, 2),
            "falling_tree": cues(20, 1),
            "fires": cues(25, 2),
            "flowers": cues(30, 3),
            "forest": cues(35, 1),
            "mushrooms": cues(43, 5),
            "storms": cues(62, 3),
        },
        "controls": control_addresses("Foreground_1"),
    },
    "bg2": {
        "cues": {
            "boreal": cues(1, 3),
            "deaad": cues(7, 2),
            "deforestation": cues(10, 2),
            "dry_pine": cues(13, 3),
            "fall": cues(16, 5),
            "falling_trees": cues(21, 1),
            "fires": cues(26, 9),
            "flowers": cues(31, 6),
            "forest": cues(36, 3),
            "mountains": cues(39, 3),
            "mushrooms": cues(44, 2),
            "rain": cues(49, 6),
            "rainforest": cues(52, 7),
            "smoke": cues(55, 5),
            "spring": cues(58, 4),
            "storms": cues(63, 3),
            "summer": cues(66, 6),
            "winter": cues(71, 5),
        },
        "controls": control_addresses("Background_2"),
    },
    "bg1": {
        "cues": {
            "boreal": cues(2, 2),
            "dead": cues(8, 5),
            "deforestation": cues(11, 2),
            "dry_pine": cues(14, 2),
            "fall": cues(17, 4),
            "falling_trees": cues(22, 1),
            "fires": cues(27, 7),
            "flowers": cues(32, 6),
            "forest": cues(37, 5),
            "mountains": cues(40, 2),
            "mushrooms": cues(45, 2),
            "rain": cues(50, 6),
            "rainforest": cues(53, 7),
            "smoke": cues(56, 5),
            "spring": cues(59, 4),
            "storms": cues(64, 2),
            "summer": cues(67, 6),
            "winter": cues(72, 6),
        },
        "controls": control_addresses("Background_1"),
    },
}


def layer_cue(layer: str, bin: str, index: int):
    return MADMAPPER_ADDRESSES[layer]["cues"][bin][index]


def control(layer: str, control: str):
    return MADMAPPER_ADDRESSES[layer]["controls"][control]
