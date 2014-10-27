# coding: utf-8
import pandas as pd
from fipser import Fipser
from pprint import pprint

f = Fipser()

df = pd.read_csv('data/fips_place_lower.csv')
lines = [x.strip() for x in df['county'].values]

a = []
[a.extend(x.split(',')) for x in lines]

b = list(set([x.strip(' "') for x in a]))
c = [f._resolve_part(x, 'county') for x in b]

leftovers = [b[i] for i,x in enumerate(c) if x == {'county': None}]

pprint(leftovers)
