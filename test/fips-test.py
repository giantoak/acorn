# coding: utf-8
import nose
import os
import sys

path = os.path.dirname(
        os.path.dirname(
            os.path.realpath(__file__)))
sys.path.append(os.path.join(path, 'preprocess'))

from fipser import Fipser

def test_get():
    fipser = Fipser()
    def run_test(level, name, precursor, result):
        r = fipser._resolve_part(level, name, precursor)
        assert r == result

    fixtures = (
            ['state', 'VA', None, '51'],
            ['state', 'Alabama', None, '01'],
            ['state', 'xxhaberdash', None, None],
            ['county', 'xxhaberdash', None, None],
            ['place', 'xxhaberdash', None, None],
            ['place', 'abbeville', '01', '00124']
            )

    for cat, name, pre, result in fixtures:
        yield run_test, cat, name, pre, result


def test_fips():
    def run_fips(f, loc, ans):
        r = f.resolve(loc)
        assert r == ans
   fipser = Fipser()
    fixtures = {
            # city state no punctuation
            'Alexandria VA': {
                'state_fips': '51',
                'place_fips': '01000',
                'county_fips': '510',
                },
            # multi-word state
            'North Dakota': {
                'state_fips': '38',
                'place_fips': None,
                'county_fips': None,
                },
            # multi-word place, multi-word state
            'Charles Mix, South Dakota': {
                'state_fips': '46',
                'place_fips': None,
                'county_fips': '023',
                },
            'Clarendon, South Carolina 29042': {
                'state_fips': '45',
                'place_fips': None,
                'county_fips': '027',
                },
            # this doesn't exist
            'Gibberish, South Carolina': {
                'state_fips': '45',
                'place_fips': None,
                'county_fips': None,
                },
            # accept "county" as suffix
            'Humboldt County, California': {
                'state_fips': '06',
                'place_fips': None,
                'county_fips': '023',
                },
            # daytona beach is encoded as daytona in census
            'Daytona, Florida': {
                'state_fips': '12',
                'place_fips': '16525',
                'county_fips': None,
                },
            }

    for loc, ans in fixtures.iteritems():
        yield run_fips, fipser, loc, ans

