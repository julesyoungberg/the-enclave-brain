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
        "flood_lights": ["green", "blue"],
    },
    "burning_forest": {
        "bg": ["fires"],
        "fg": ["fires", "smoke"],
        "flood_lights": ["red", "orange"],
        "max_length": 48,
        "min_length": 20,
    },
    "dead_forest": {
        "bg": ["dead"],
        "fg": ["smoke"], #, "fires"]
        "fg_blackout": 0.9,
        "flood_lights": ["brown", "grey"],
    },
    "growing_forest": {
        "bg": ["growth", "mushrooms"],
        "fg": ["rain", "mushrooms", "flowers"],
        "fg_blackout": 0.5,
        "flood_lights": ["green", "blue"],
        "max_length": 50,
        "min_length": 20,
        "more_health_is_longer": True,
    },
    "climate_change": {
        "bg": ["dry_pine", "drought", "smoke"],
        "fg": ["fires", "smoke"], # "storms"],
        "flood_lights": ["orange", "grey"],
        "max_length": 60,
        "min_length": 20,
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
        "flood_lights": ["brown", "red"],
        "max_length": 48,
        "min_length": 20,
    },
    "rain": {
        "bg": ["rain"],
        "fg": ["rain"],
        "flood_lights": ["teal", "indigo"],
        "max_length": 48,
        "min_length": 20,
        "more_health_is_longer": True,
    },
    "storm": {
        "bg": ["storms"],
        "fg": ["storms"],
        "flood_lights": ["blue", "purple"],
        "max_length": 60,
        "min_length": 30,
    },
}
