import pandas as pd
#
# At first I got ValueError: Trailing data. I added lines=True.
df = pd.read_json('aggregated.json', lines=True)
df.drop(['_id', 'microwave'], axis=1, inplace=True)
df_pickled = df.to_pickle('aggregated.pkl')
