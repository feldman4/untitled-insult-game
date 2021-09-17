"""Helpful utility methods."""

import pandas as pd

import os
from typing import Union

from game.cfg import dataframe_to_grammar
from game.constants import VOCAB_CSV, VOCAB_XLSX_URL, VOCAB_XLSX


def calc_similarity_modifier(previous_responses: list, new_response: str) -> Union[int, float]:
    """Determines how similar new response is to previously heard ones and returns a modifier to be applied to damage.

    If insult is new, returns 1.
    """
    if not previous_responses:  # First insult
        return 1

    else:  # Need to check and calculate
        pass


def read_vocab(input_filter: str = None) -> pd.DataFrame:
    """Downloads the vocab CSV if not there and returns the dataframe. Can filter the DF by input type."""
    import os

    if not os.path.isfile(VOCAB_CSV):
        update_vocab()

    df = pd.read_csv(VOCAB_CSV)
    if input_filter:
        if input_filter not in set(df.input):
            raise ValueError(f"Invalid input filter option passed! Please choose from: {set(df.input)}")

        df = df.loc[df["input"] == input_filter]

    return df


def update_vocab():
    """Download vocabulary from google sheet."""
    import requests
    print(f'Downloading from: {VOCAB_XLSX_URL}')

    r = requests.get(VOCAB_XLSX_URL)
    with open(VOCAB_XLSX, 'wb') as fh:
        fh.write(r.content)
    (pd.read_excel(VOCAB_XLSX, sheet_name=0)
     .pipe(validate_vocab)
     .to_csv(VOCAB_CSV, index=None))

    print(f'Saved vocab xlsx to {VOCAB_XLSX}')
    print(f'Saved first sheet to {VOCAB_CSV}')


def validate_vocab(df_vocab):
    assert len(df_vocab.columns) == len(set(df_vocab.columns))
    assert 'input' in df_vocab
    assert 'output' in df_vocab
    return df_vocab


def update_vocab_and_vectors():
    """Download vocabulary, then update word vector file."""
    from game.word_handling import update_insult_vectors
    update_vocab()
    update_insult_vectors()


def load_vocab():
    return pd.read_csv(VOCAB_CSV)


def get_grammar(query_string: str):
    """Returns grammar that player/enemy can use"""
    return load_vocab().query(query_string).pipe(dataframe_to_grammar)


def get_dmg_map() -> dict:
    return load_vocab().set_index('output')['damage'].dropna().to_dict()

