# this file contains scene configuration
# each scene consists of a background cue bin and select foregrounds

SCENES = {
    "healthy_forest": {
        "bg": ["boreal", "fall", "mountains", "rainforest"],
        "fg": ["birds", "flowers"],
    },
    "dying_forest": {
        "bg": ["deforestation", "dry_pine", "smoke", "storms"],
        "fg": ["falling_trees", "storms"],
    },
    "dead_forest": {
        "bg": ["dead", "fires"],
        "fg": ["falling_trees", "fires", "storms"],
    },
    "recovering_forest": {
        "bg": ["mushrooms", "rain"],
        "fg": ["mushrooms", "rain"],
    },
}
