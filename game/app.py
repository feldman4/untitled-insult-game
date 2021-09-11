import fire
import sys


def term():
    from game import term
    term.run()


def server():
    from game import server
    server.run()


def update_vocab():
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


if __name__ == '__main__':
    fire.Fire()
