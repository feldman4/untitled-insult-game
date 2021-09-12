"""Helpful utility methods."""

import os

import pandas as pd

from game.constants import VOCAB_FILE


def read_vocab(input_filter: str = None) -> pd.DataFrame:
    """Downloads the vocab CSV if not there and returns the dataframe. Can filter the DF by input type."""
    if not os.path.isfile(VOCAB_FILE):
        update_vocab()

    df = pd.read_csv(VOCAB_FILE)
    if input_filter:
        if input_filter not in set(df.input):
            raise ValueError(f"Invalid input filter option passed! Please choose from: {set(df.input)}")

        df = df.loc[df["input"] == input_filter]

    return df


def update_vocab():
    """Download vocabulary from google sheet."""

    sheet_id = '1lkxMe_MYYsi8ecTe-otTqaHLAuM0Mu2ALTNaIzZANrI'
    sheet_name = 'grammars'
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&sheet={sheet_name}'

    pd.read_csv(url).to_csv(VOCAB_FILE, index=None)

    print(f'Loaded vocab to {VOCAB_FILE}')
    print(f'Google link: {url}')


def update_vocab_and_vectors():
    from game.word_handling import update_insult_vectors
    update_vocab()
    update_insult_vectors()
