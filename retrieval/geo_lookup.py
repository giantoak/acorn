from __future__ import print_function
from acser import Acser
import pandas as pd
import sys
import numpy as np
# tags a csv file from stdin with geoids
# writes to stdout


def fix_format(cell, digits):
    if np.isnan(cell):
        return None
    else:
        return str(int(cell)).zfill(digits)

# XXX: change these to not be hard-coded, and this can become generalizable:
def geo_lookup(row):
    statefp = fix_format(row['state_fips'], 2)
    countyfp = fix_format(row['county_fips'], 3)
    placefp = fix_format(row['place_fips'], 5)
    try:
        print('Place: {}, {}, C: {}, P: {}'.format(row['place'], statefp,
            countyfp, placefp), file=sys.stderr)
        g = a.geo_lookup(statefp, countyfp, placefp)
    except ValueError:
        return ''
    return g

if __name__ == '__main__':
    a = Acser()

    df = pd.read_csv(sys.stdin)

    df['gid'] = df.apply(geo_lookup, 1)

    df.to_csv(sys.stdout, index=False)
