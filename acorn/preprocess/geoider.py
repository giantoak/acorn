import pandas as pd
import sys
import os

sys.path.append(os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.realpath(__file__))),
        'retrieval'))

from fipser import Fipser
from acser import Acser

class Geoider(object):

    def __init__(self):
        self.fipser = Fipser()
        self.acser = Acser()

    def tag(self, fh, col, header=False):
        df = pd.read_csv(fh)
        
        geos = []
        for i, row in df.iterrows():
            ans = self.fipser.resolve(row[col])
            
            try:
                geo = self.acser.geo_lookup(ans['state_fips'], ans['county_fips'], 
                        ans['place_fips'])
            except ValueError:
                geo = None
            geos.append(geo)
            #ans['geoid'] = geo
        #    print query, ans
            #resolved.append(ans)
        
        return pd.Series(geos, name='geoid')
        #df_results = pd.DataFrame(resolved)
        #df_results = pd.concat([df_results, df], axis=1)
        #return df_results

if __name__ == '__main__':
    geo = Geoider()
    df = geo.tag(sys.stdin, sys.argv[1])
    df.to_csv(sys.stdout, index=False)

