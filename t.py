# from urllib.parse import quote

# quote('문형태')

import pandas as pd

df = pd.read_csv(r'/home/fakeblocker/code/python/aucapi/seoul_final.csv')

df.sample(6).to_dict(orient='records')
month = 3
res = df.sample(n=month)
res.to_dict(orient='records')