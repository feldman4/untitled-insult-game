import pandas as pd

# URLs
TWINE_ARCHIVE = 'DF/worlds/*.html'
VOCAB_FILE = "resources/vocab.csv"

# Server settings
PORT = 1241
TIMEOUT = 0.01

# String constants
REWIND = 'REWIND'
FFORWARD = 'FFORWARD'
SYNCHRONIZE = 'SYNCHRONIZE'

# Modifiers
VULNERABLE_MODIFIER = 1.5

# Server messages
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

# Mappers
level_mapper = {  # Level: Experience needed to reach that level
    1: 0,
    2: 30,
    3: 90,
    4: 270,
    5: 650,
    6: 1400,
}