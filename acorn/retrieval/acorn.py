#!/usr/bin/python
from __future__ import print_function

import argparse
import os
import sys
from pprint import pprint

dirroot = os.path.dirname(
        os.path.dirname(
            os.path.realpath(__file__)))

sys.path.extend([os.path.join(dirroot, 'retrieval'),
    os.path.join(dirroot, 'preprocess')])

from acser import Acser
from fipser import Fipser

class Acorn(object):
    def __init__(self):
        self.fips = Fipser()
        self.acs = Acser()
   
    def resolve(self, loc, schema=None):
        f = self.resolve_fips(loc)
        g = self.resolve_geo(f, schema)
        
        return {'fips': f,
                'geoid': g}

    def resolve_fips(self, loc):
        f = self.fips.resolve(loc)
        return f

    def resolve_geo(self, fips, schema=None):
        s, c, p = fips['state_fips'], fips['county_fips'], fips['place_fips']
        g = self.acs.geo_lookup(s, c, p, schema)
        
        return g

def _get_args():
    parser = argparse.ArgumentParser(description='Resolve a place name into FIPS \
            Codes and GeoID')
    parser.add_argument('place', metavar='loc', type=str,
                            help='A string of the location to resolve')
    
    parser.add_argument('--schema', nargs='?', type=str, 
            default=None, help='The schema to use to resolve geoheaders.')

    args = parser.parse_args()
    return args

def main():
    ac = Acorn()
    args = _get_args()
    
    result = ac.resolve(args.place, args.schema)

    print(args.place, args.schema)
    print('\t', end='')
    pprint(result, indent=2)

if __name__ == '__main__':
    main()
