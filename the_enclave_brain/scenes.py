# this file contains scene configuration
# each scene consists of a background cue bin and select foregrounds

MAIN_SCENES = [
    "healthy_forest",
    "burning_forest",
    "dead_forest",
    "growing_forest",
]

EVENTS = ["climate_change", "deforestation", "rain", "storm"]


SCENES = {
    "healthy_forest": {
        "bg": ["boreal", "forest", "mountains", "rainforest", "flowers", "summer"],
        "fg": ["birds"],
        "fg_blackout": 0.9,
    },
    "burning_forest": {
        "bg": ["fires"],
        "fg": ["fires", "smoke"],
    },
    "dead_forest": {
        "bg": ["dead"],
        "fg": ["fires", "smoke"],
        "fg_blackout": 0.9,
    },
    "growing_forest": {
        "bg": ["growth", "mushrooms"],
        "fg": ["rain", "mushrooms", "flowers"],
        "fg_blackout": 0.5,
    },
    "climate_change": {
        "bg": ["dry_pine", "drought", "smoke"],
        "fg": ["fires", "smoke"], # "storms"],
    },
    "deforestation": {
        "bg": [
            "deforestation",
            "pollution",
            "industry",
            "roads",
            "logging",
        ],
        "fg": ["smoke"],
        "fg_blackout": 0.8,
    },
    "rain": {
        "bg": ["rain"],
        "fg": ["rain"],
    },
    "storm": {
        "bg": ["storms"],
        "fg": ["storms"],
    },
}
