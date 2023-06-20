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
        "fg_blackout": 0.75,
        "lights": ["green_and_blue"],
        "audio": [],
    },
    "burning_forest": {
        "bg": ["fires"],
        "fg": ["fires", "smoke"],
        "lights": ["red_and_orange"],
        "audio": [],
    },
    "dead_forest": {
        "bg": ["dead"],
        "fg": ["falling_trees", "fires", "storms"],
        "lights": ["brown_and_gray"],
        "audio": [],
    },
    "climate_change": {
        "bg": ["dry_pine", "drought"],
        "fg": ["storms", "smoke", "fires"],
        "lights": ["orange_and_gray"],
        "audio": [],
    },
    "deforestation": {
        "bg": [
            "deforestation",
            "pollution",
            "industry",
            "roads",
        ],
        "fg": ["storms", "falling_trees"],
        "lights": ["red_and_brown"],
        "audio": [],
    },
    "rain_forest": {
        "bg": ["mushrooms", "rain"],
        "fg": ["mushrooms", "rain"],
        "lights": ["green_and_blue"],
        "audio": [],
    },
    "storm_forest": {
        "bg": ["storms"],
        "fg": ["storms"],
        "lights": ["blue_and_purple"],
        "audio": [],
    },
}
