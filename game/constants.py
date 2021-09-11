PORT = 1241
TIMEOUT = 0.01

START = 'fire it up'

INTELLIGENCE = "intelligence"
WEIGHT = "weight"
PERSONALITY = "personality"

vocab_dict = {
    1: {
        "idiot": (3, INTELLIGENCE),
        "fatso": (5, WEIGHT),
        "streber": (7, PERSONALITY),
    },
    2: {
        "swine": (6, WEIGHT),
        "ignoramous": (5, INTELLIGENCE),
        "pariah": (7, PERSONALITY)
    },
}

level_mapper = {
    1: 0,
    2: 30,
    3: 90,
    4: 270,
    5: 650,
    6: 1400,
}