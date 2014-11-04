from __future__ import print_function
import pandas as pd
import sys
import os
import re
import numpy as np
import requests
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker
import urllib
from collections import defaultdict
import grequests

sys.path.append(os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__))))

try:
    from dbconfig import dburl

except ImportError:
    raise Exception('Need a file called dbconfig.py in same directory as this \
            file, that defines connection url `dburl`')

class Gazetteer(object):
    """
    A converter from ambiguous place names to FIPS codes.
    """
    gaz_places = 'gaz.places'
    gaz_counties = 'gaz.counties'
    census_reporter = 'http://api.censusreporter.org/1.0/geo/elasticsearch?'

    def __init__(self):
        # connect to ACS database
        engine = sqlalchemy.create_engine(dburl)
        Session = scoped_session(sessionmaker(bind=engine))
        self.s = Session()


        return

    def resolve_many(self, names, verbose=False):
        """asynchronously query Census Reporter API with all names"""
        

    def resolve(self, name, sum_level=None, verbose=False):
        """Return ACS data for given columns
        at the given geo ID.

        """
        
        # check if lowercase name is in places db
        """
        lowername = name.lower()
        q = self.s.execute('SELECT * FROM :table WHERE placename=:name', 
                {   'table': self.gaz_places,
                    'name': lowername })

        n = q.first()
        if n:
            ndict = {k:v for k,v in row.items()}
            result = {
                    'geoid': ndict['geoid'],
                    'name': ndict['placename'],
                    }
            """

         # store results into results struct and return it

        # query census API
        params = {'q': name, 'size': 1}

        if sum_level:
            params.update({'sumlevs': sum_level})
        url = self.census_reporter + urllib.urlencode(params)
        r = requests.get(url)
        return r.json()['results'][0]

        
