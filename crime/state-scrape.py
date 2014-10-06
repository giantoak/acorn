# coding: utf-8

# fetch the min/max ccids for all the states

from __future__ import print_function
from crime import fetch_ccids
import json
import pdb

if __name__ == '__main__':
    state_ranges = {}
    for i in range(1, 52):
        ids = fetch_ccids(i)
        state_ranges[i] = ids

        print('Scraped state {i}: len {length}, min {m}'.format(i=i,
            length=len(ids), m=min(ids)))
    
    with open('ccids_by_state.json', 'w') as f:
        json.dump(state_ranges, f)


    pdb.set_trace()
