from __future__ import print_function
from acorn import Acorn
import sys
import pandas as pd

df = pd.read_csv(sys.stdin, dtype=object)
a = Acorn()

for i, row in df.iterrows():
    name = row[sys.argv[1]]
    try:
        r = a.resolve(name)
        df.loc[i, 'gid'] = r['geoid']
    except ValueError:
        print(name, file=sys.stderr)
    

df.to_csv(sys.stdout, index=False)
