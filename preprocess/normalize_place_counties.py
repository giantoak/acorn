# coding: utf-8
import pandas as pd
from fipser import Fipser
import sys
# reads in fips_place_lower.csv in stdin, pipes out normalized place-county 
# table

f = Fipser()

def normalize(cell):
    return [x.strip(' "') for x in cell.split(',')]

def uniq(li):
    return list(set(li))

df = pd.read_csv(sys.stdin, dtype=object)
lines = [x.strip() for x in df['county'].values]

a = []
[a.extend(x.split(',')) for x in lines]

b = uniq([x.strip(' "') for x in a])
c = [f._resolve_part('county', x) for x in b]

county_fips = {b[i]: x for i,x in enumerate(c)}
plco = []
for i, row in df.iterrows():
    nrmc = normalize(row['county'])
    cfs = uniq([county_fips[co] for co in nrmc])
    for cf in cfs:
        plco.append({'placefp': row['placefp'], 'countyfp': cf})

dfplco = pd.DataFrame(plco)

dfplco.to_csv(sys.stdout, index=False, columns=('placefp', 'countyfp'))
