import fire
import sys


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
    local = 'resources/vocab.csv'

    sheet_id = '1lkxMe_MYYsi8ecTe-otTqaHLAuM0Mu2ALTNaIzZANrI'
    sheet_name = 'grammars'
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    (pd.read_csv(url)
    .dropna(axis=1, how='all')
    .to_csv(local, index=None))
    print(f'Loaded vocab to {local}')
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
