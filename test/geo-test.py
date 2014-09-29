import pandas as pd
import sys
import os

sys.path.append(os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.realpath(__file__))),
    'preprocess'))

from geoider import Geoider

def test_tagger():
    geo = Geoider()
    df = geo.tag('crime_scrape2013_full_names_sample.csv', 'full_name')
    
    assert df
