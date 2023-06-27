# this file contains scene configuration
# each scene consists of a background cue bin and select foregrounds

MAIN_SCENES = [
    "healthy_forest",
    "burning_forest",
    "dead_forest",
    "regrowth",
]

EVENTS = ["climate_change", "deforestation", "rain_forest", "storm_forest"]


SCENES = {
    "healthy_forest": {
        "bg": ["boreal", "forest", "mountains", "rainforest", "flowers", "summer"],
        "fg": ["birds", "mushrooms"],
        "fg_blackout": 0.67,
    },
    "burning_forest": {
        "bg": ["fires"],
        "fg": ["fires", "smoke"],  # , "falling_trees"],
    },
    "dead_forest": {
        "bg": ["dead", "deforestation"],
        "fg": ["storms", "smoke"],  # , "falling_trees"],
        "fg_blackout": 0.5,
    },
    "climate_change": {
        "bg": ["dry_pine", "drought"],
        "fg": ["storms", "smoke", "fires"],
    },
    "deforestation": {
        "bg": [
            "deforestation",
            "pollution",
            "industry",
            "roads",
            "logging",
        ],
        # @todo create more appropriate foreground cues from some of bg content
        "fg": ["storms"],  # "falling_trees"],
        "fg_blackout": 0.5,
    },
    "rain_forest": {
        "bg": ["rain"],
        "fg": ["rain"],
    },
    "storm_forest": {
        "bg": ["storms"],
        "fg": ["storms"],
    },
    "regrowth": {
        "bg": ["growth", "mushrooms"],
        "fg": ["rain", "mushrooms"],
        "fg_blackout": 0.5,
    },
}
