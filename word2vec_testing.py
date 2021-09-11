import pandas as pd


sheet_id = '1lkxMe_MYYsi8ecTe-otTqaHLAuM0Mu2ALTNaIzZANrI'
sheet_name = 'grammars'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

print(pd.read_csv(url))