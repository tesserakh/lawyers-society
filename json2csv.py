import pandas as pd
pd.read_json('lawyers.json').to_csv('lawyers.csv', index = False)
