import pandas as pd

TWINE_ARCHIVE = 'DF/worlds/*.html'

PORT = 1241
TIMEOUT = 0.01

REWIND = 'REWIND'
FFORWARD = 'FFORWARD'
SYNCHRONIZE = 'SYNCHRONIZE'

LOAD_1 = 'LOAD 1'
LOAD_2 = 'LOAD 2'
LOAD_3 = 'LOAD 3'
LOAD_4 = 'LOAD 4'

LOAD_SIGNALS = LOAD_1, LOAD_2, LOAD_3, LOAD_4

# shortcuts from front-end
SYSTEM_CODES = {
    '1': LOAD_1,
    '2': LOAD_2,
    '3': LOAD_3,
    '4': LOAD_4,
    '7': REWIND,
    '8': FFORWARD,
    '9': SYNCHRONIZE,
}

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