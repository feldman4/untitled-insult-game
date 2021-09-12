import gensim
import math
import pandas as pd
import numpy as np


# Initialize database
def init_word_scores():
    import gensim.downloader as api
    return api.load('glove-twitter-25')


def calc_similarity(word1: str, word2: str) -> float:
    """Calculate the similarity between two insults/words"""
    dic = load_insults_vectors()
    return round(abs(sum(dic[word1] / (sum(dic[word1] ** 2) ** 0.5) * dic[word2] / (sum(dic[word2] ** 2) ** 0.5))), 4)


def create_ranking(word: str) -> list:
    """Calculate rank of insult compared to all other insults that you can use"""
    dic = load_insults_vectors()
    l = []
    for x in dic.keys():
        l.append((x, calc_similarity(word, x)))
    l_s = sorted(l, key=lambda y: y[1])
    return [p[0] for p in l_s]


def calc_total_dmg_mod(word1: str, word2: str) -> float:
    """Calculate damage modifier for two words, always between 0 and 2"""
    ranking = create_ranking(word2)
    ranking_mod = math.log10(ranking.index(word1) + 0.001) / math.log10(len(ranking))
    similarity_mod = calc_similarity(word1, word2)

    return round((ranking_mod + similarity_mod) /2, 3)


def multi_word_dmg(attack: list, defense: list) -> float:
    """If multiple words hit"""
    l = []
    for word1 in attack:
        for word2 in defense:
            l.append(calc_total_dmg_mod(word1, word2))
    return round(sum(l) / len(l), 3)


def update_insult_vectors():
    """Update insult vector list spreadsheet got updated"""

    model = init_word_scores()
    df = pd.read_csv('resources/vocab.csv')

    with open('resources/insult_vectors.csv', 'w') as handle:
        for ins in df[df.rule == 'vocabulary']['output']:
            if ins.lower() in model:
                handle.write(f'{ins}')
                for num in model[ins]:
                    handle.write(f'\t{num}')
                handle.write(f'\n')


def load_insults_vectors() -> dict :
    """Reads local insults vector file and return dictionary with words as keys and vectors as values"""
    df = pd.read_csv('resources/insult_vectors.csv', delimiter='\t', header=None, index_col=0).T
    return {col: df[col].values for col in df}
