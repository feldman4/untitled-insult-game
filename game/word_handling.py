import gensim
import math
import pandas as pd
import numpy as np


# Initialize database
def init_word_scores():
    import gensim.downloader as api
    return api.load('glove-twitter-25')


def score_words(attack_word: str, defense_word: str, model: gensim.models.keyedvectors.KeyedVectors) -> float:
    """Calculates similarity between the two input words, or an input sentence and a word based on the input model"""

    pd.read_csv('resources/insult_vectors.csv', delimiter='\t', header=None)

    # Adjust words to lowercase
    defe = defense_word.lower()
    attk = attack_word.lower().replace('-', ' ').split()

    # Calculate similarity
    sim = model.similarity(attk, defe)

    # Calculate global word ranks
    ranks = [1 - (model.rank(a, defe) / len(model)) for a in attk]
    mean_ranks = (sum(ranks) * 100 / len(ranks))

    # Return rounded rank weighted similarity
    return round(abs((sum(sim) / len(sim)) * math.log10(mean_ranks)), 3)


def update_insult_vectors():
    """Update insult vector list spreadsheet got updated"""

    model = init_word_scores()
    df = pd.read_csv('resources/vocab.csv')

    with open('resources/insult_vectors.csv', 'w') as handle:
        for ins in df[df.rule == 'vocabulary']['output']:
            if ins in model:
                handle.write(f'{ins}')
                for num in model[ins]:
                    handle.write(f'\t{num}')
                handle.write(f'\n')


def load_insults_vectors() -> dict :
    """Reads local insults vector file and return dictionary with words as keys and vectors as values"""
    df = pd.read_csv('resources/insult_vectors.csv', delimiter='\t', header=None, index_col=0)
    return {ind: np.array(row) for ind, row in df.iterrows()}
