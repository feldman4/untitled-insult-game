import pandas as pd

PORT = 1241
TIMEOUT = 0.01

START = 'fire it up'

INTELLIGENCE = "intelligence"
WEIGHT = "weight"
PERSONALITY = "personality"


vocab_dict = pd.DataFrame(
    [
        {"word": "idiot", "level": 1, "damage": 3, "damage_type": INTELLIGENCE},
        {"word": "fatso", "level": 1, "damage": 5, "damage_type": WEIGHT},
        {"word": "streber", "level": 1, "damage": 7, "damage_type": PERSONALITY},
        {"word": "swine", "level": 2, "damage": 6, "damage_type": WEIGHT},
        {"word": "ignoramous", "level": 2, "damage": 5, "damage_type": INTELLIGENCE},
        {"word": "pariah", "level": 2, "damage": 7, "damage_type": PERSONALITY},
    ]
)

level_mapper = {
    1: 0,
    2: 30,
    3: 90,
    4: 270,
    5: 650,
    6: 1400,
}