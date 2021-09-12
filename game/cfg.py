from collections import defaultdict
import pandas as pd

from game.cfg_python import is_complete, choices, constructs, extend
from game.constants import VOCAB_FILE

def dataframe_to_grammar(df_vocab):
    """Convert a (filtered) vocabulary table into a grammar.
    """    
    grammar = defaultdict(list)
    for a, b in df_vocab[['input', 'output']].values:
        grammar[a].append(b.replace(',', ' '))
    return grammar


def load_grammar_level2():
    df_vocab = pd.read_csv(VOCAB_FILE).query('level <= 2')
    return dataframe_to_grammar(df_vocab)


def get_all_insults(grammar):
    return [' '.join(x) for x in extend(grammar, ['S'])]