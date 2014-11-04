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

from gazetteer import Gazetteer

class AcornCR(object):
    def __init__(self):
        self.gazzer = Gazetteer()
   
    def resolve(self, loc, sumlev=None):
        g = self.gazzer.resolve(loc, sumlev)
        
        return g

def _get_args():
    parser = argparse.ArgumentParser(description='Resolve a place name into FIPS \
            Codes and GeoID')
    parser.add_argument('place', metavar='loc', type=str,
                            help='A string of the location to resolve')
    
    parser.add_argument('--sumlev', nargs='?', type=str, 
            default=None, help='The 3-digit summary level (optional)')

    args = parser.parse_args()
    return args

def main():
    ac = AcornCR()
    args = _get_args()
    
    result = ac.resolve(args.place, args.sumlev)

    print(args.place, args.sumlev)
    print('\t', end='')
    pprint(result, indent=2)

if __name__ == '__main__':
    main()
