# this file contains scene configuration
# each scene consists of a background cue bin and select foregrounds

MAIN_SCENES = [
    "healthy_forest",
    "burning_forest",
    "dead_forest",
]

EVENTS = ["climate_change", "deforestation", "rain_forest", "storm_forest"]


SCENES = {
    "healthy_forest": {
        "bg": ["boreal", "forest", "mountains", "rainforest", "flowers", "summer"],
        "fg": ["birds", "mushrooms"],
        "fg_blackout": 0.67,
        "audio": [],
    },
    "burning_forest": {
        "bg": ["fires"],
        "fg": ["fires", "smoke"],  # , "falling_trees"],
        "audio": [],
    },
    "dead_forest": {
        "bg": ["dead"],
        "fg": ["storms", "smoke"],  # , "falling_trees"],
        "fg_blackout": 0.5,
        "audio": [],
    },
    "climate_change": {
        "bg": ["dry_pine", "drought"],
        "fg": ["storms", "smoke", "fires"],
        "audio": [],
    },
    "deforestation": {
        "bg": [
            "deforestation",
            "pollution",
            "industry",
            "roads",
        ],
        # @todo create more appropriate foreground cues from some of bg content
        "fg": ["storms"],  # "falling_trees"],
        "fg_blackout": 0.5,
        "audio": [],
    },
    "rain_forest": {
        "bg": ["mushrooms", "rain", "rainforest"],
        "fg": ["mushrooms", "rain"],
        "audio": [],
    },
    "storm_forest": {
        "bg": ["storms"],
        "fg": ["storms"],
        "audio": [],
    },
}
