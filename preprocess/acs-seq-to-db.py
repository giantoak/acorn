import pandas as pd

df = pd.read_csv('acs-seq-lookup.csv')

df2 = df[['Table ID', 'Sequence Number']]
