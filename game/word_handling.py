import gensim
import math


# Initialize database
def init_word_scores():
    import gensim.downloader as api
    return api.load('glove-twitter-25')


def score_words(attack_word: str, defense_word: str, model: gensim.models.keyedvectors.KeyedVectors) -> float:
    """Calculates similarity between the two input words, or an input sentence and a word based on the input model"""

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
