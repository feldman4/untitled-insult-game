from collections import defaultdict
import pandas as pd

from game.cfg_python import is_complete, choices, constructs, extend
from game.constants import VOCAB_CSV


example_grammar = {
    'S': ['NP'],
    'NP': ['N', 'A N'],
    'A': ['Lonely', 'Disguised', 'Unsuccessful', 'Alcoholic', 'Spineless', 
          'Impotent', 'Mean', 'Overpaid'],
    'N': ['Dwarf', 'Fool', 'Wimp', 'Assassin', 'Accomplice', 'Pimp', 'Sidekick', 
          'Molestor', 'Dog', 'Narcissist', 'Boob'],
    'NPL': ['Liars', 'Thugs'],
    }


def dataframe_to_grammar(df_vocab):
    """Convert a (filtered) vocabulary table into a grammar.
    """    
    grammar = defaultdict(list)
    for a, b in df_vocab[['input', 'output']].values:
        grammar[a].append(b.replace(',', ' '))
    return grammar


def get_all_insults(grammar):
    """All sentences in grammar.
    """
    return [' '.join(x) for x in extend(grammar, ['S'])]