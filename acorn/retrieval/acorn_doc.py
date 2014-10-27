from __future__ import print_function
from acorn import Acorn
import sys
import pandas as pd

df = pd.read_csv(sys.stdin, dtype=object)
a = Acorn()
try:
    arg = sys.argv[1:]
except IndexError:
    print('Error: argument required.', file=sys.stderr)
    sys.exit()

for i, row in df.iterrows():
    if len(arg) == 1:
        name = row[arg[0]]
    elif len(arg) > 1:
        name = reduce(lambda x, y: x + ', '+ y, row[arg])
    try:
        r = a.resolve(name)
        df.loc[i, 'gid'] = r['geoid']
    except ValueError:
        print(name, file=sys.stderr)
    

df.to_csv(sys.stdout, index=False)
