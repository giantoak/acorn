# coding: utf-8
from __future__ import print_function
from crime import fetch_by_ccid
import json

with open('ccids_by_state.json', 'r') as f:
    state_ccids = json.load(f)

for state, ccids in state_ccids.iteritems():
    r = fetch_by_ccid(ccids)

    with open('scraped/crime_by_precinct_{}.csv'.format(state), 'w') as f:
        f.write(r)

    print('Fetched state {}'.format(state))
