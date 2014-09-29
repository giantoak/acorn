from __future__ import print_function

from acser import Acser
import pandas as pd
import sys
import numpy as np

qs = ["B01001_001","B19013_001","B01001A_001","B01001B_001","B15002_003",
        "B15002_004","B15002_005","B15002_006","B15002_007","B15002_008",
        "B15002_009","B15002_010","B15002_011","B15002_012","B15002_013",
        "B15002_014","B15002_015","B15002_016","B15002_017","B15002_018"]

df = pd.read_csv('data/locations_resolved.csv', dtype=object)
df2 = df.where((pd.notnull(df)), None)
a = Acser()

results = []
for i, row in df2.iterrows():
    try:
        statefp = row['state_fips'] 
        countyfp = row['county_fips']
        placefp = row['place_fips'] 

        geo_id = a.geo_lookup(statefp, countyfp, placefp)
    except ValueError:
        print('{}-{}-{} didn\'t resolve to a geoid'.format(statefp, countyfp,
            placefp), file=sys.stderr)
        continue
    
    result = {'place': row['url'][1:]}
    acs_data = a.retrieve(geo_id, qs)
    acs_data.update(result)

    results.append(acs_data)

df_out = pd.DataFrame(results)
df_out.to_csv(sys.stdout, index=False)

