# this file contains scene configuration
# each scene consists of a background cue bin and select foregrounds

SCENES = {
    "healthy_forest": {
        "bg": ["boreal", "fall", "mountains", "rainforest"],
        "fg": ["birds", "flowers"],
    },
    "deforestation": {
        "bg": [
            "deforestation",
            "dry_pine",
            "pollution",
            "industry",
            "drought",
            "roads",
        ],
        "fg": ["storms", "fires", "falling_trees"],
    },
    "burning_forest": {
        "bg": ["deforestation", "fires"],
        "fg": ["fires", "smoke"],
    },
    "dead_forest": {
        "bg": ["dead", "fires"],
        "fg": ["falling_trees", "fires", "storms"],
    },
    "storm_forest": {
        "bg": ["storms"],
        "fg": ["storms"],
    },
    "rain_forest": {
        "bg": ["mushrooms", "rain"],
        "fg": ["mushrooms", "rain"],
    },
}
