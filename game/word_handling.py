import math
import pandas as pd

from game.constants import VOCAB_CSV, VECTOR_FILE


def load_insults_vectors() -> dict :
    """Reads local insults vector file and return dictionary with words as keys and vectors as values"""
    f = 'resources/insult_vectors.csv'
    df = pd.read_csv(f, delimiter='\t', header=None, index_col=0).T
    # some duplicates snuck in
    keep = ~df.columns.duplicated()
    df = df.iloc[:, keep]
    return {col: df[col].values for col in df}

dic = load_insults_vectors()


# Initialize database
def init_word_scores():
    import gensim.downloader as api
    return api.load('glove-twitter-25')


def calc_similarity(word1: str, word2: str) -> float:
    """Calculate the similarity between two insults/words"""
    return round(abs(sum(dic[word1] / (sum(dic[word1] ** 2) ** 0.5) * dic[word2] / (sum(dic[word2] ** 2) ** 0.5))), 4)


def create_ranking(word: str) -> list:
    """Calculate rank of insult compared to all other insults that you can use"""
    l = []
    for x in dic.keys():
        l.append((x, calc_similarity(word, x)))
    l_s = sorted(l, key=lambda y: y[1])
    return [p[0] for p in l_s][::-1]


def calc_total_dmg_mod(word1: str, word2: str) -> float:
    """Calculate damage modifier for two words, always between 0 and 2"""
    ranking = create_ranking(word2)
    on_target = math.log10(1 + ranking.index(word1))
    everything = math.log10(len(ranking))

    ranking_mod = 1 - on_target / everything
    similarity_mod = calc_similarity(word1, word2)
    return round((ranking_mod + similarity_mod) /2, 3)


def multi_word_dmg(attack: list, defense: list) -> float:
    """If multiple words hit"""
    assert 0 < len(attack)
    assert 0 < len(defense)
    l = []
    for word1 in attack:
        for word2 in defense:
            l.append(calc_total_dmg_mod(word1, word2))
    return round(sum(l), 3)


def update_insult_vectors():
    """Update insult vector list spreadsheet got updated"""

    model = init_word_scores()
    df = pd.read_csv(VOCAB_CSV)

    with open(VECTOR_FILE, 'w') as handle:
        for ins in df[df.rule == 'vocabulary']['output']:
            if ins.lower() in model:
                handle.write(f'{ins}')
                for num in model[ins]:
                    handle.write(f'\t{num}')
                handle.write(f'\n')



