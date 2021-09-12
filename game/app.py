import fire
import sys

from game.constants import VOCAB_FILE


def term():
    """curtsies front end
    """
    from game import term
    term.run()


def server():
    from game import server
    server.run()


def update_vocab():
    """Download vocabulary from google sheet.
    """
    import pandas as pd

    sheet_id = '1lkxMe_MYYsi8ecTe-otTqaHLAuM0Mu2ALTNaIzZANrI'
    sheet_name = 'grammars'
    download_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    browser_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/edit'

    # https://docs.google.com/spreadsheets/d/{sheet_id}/edit#gid=409890937

    (pd.read_csv(download_url)
    .dropna(axis=1, how='all')
    .to_csv(VOCAB_FILE, index=None))
    print(f'Loaded vocab to {local}')
    print(f'From google sheet: {browser_url}')
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&sheet={sheet_name}'

    pd.read_csv(url).to_csv(VOCAB_FILE, index=None)

    print(f'Loaded vocab to {VOCAB_FILE}')
    print(f'Google link: {url}')


def update_vocab_and_vectors():
    from game.word_handling import update_insult_vectors
    update_vocab()
    update_insult_vectors()


def twine():
    import subprocess
    from glob import glob

    files = glob('DF/twine/*html')
    for f in files:
        print(f'Converting {f}')
        subprocess.check_output(['twine_graph', f])


if __name__ == '__main__':
    fire.Fire()
