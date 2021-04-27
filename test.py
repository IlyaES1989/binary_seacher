import requests
from random import uniform

test_data = ('0000qtZc3F', 'aTlK8A8gMm', '3nF6FijOVA', 'Q2RgLO85tR', '0000qtZc3F', 'zzzzJtUDad', 'T5116l54qW',
             'dtZUeXFEEc', 'NbOFDESwLU','ZwtlwveECC')

for sku in test_data:
    rank = round(uniform(0.1, 1.0), 1)
    url = 'http://localhost:8000/'

    resp = requests.get(url)

    print(resp.status_code)