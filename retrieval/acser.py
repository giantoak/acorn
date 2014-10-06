from __future__ import print_function
import pandas as pd
import sys
import os
import re
import numpy as np

import psycopg2
from psycopg2 import InternalError, ProgrammingError
from collections import defaultdict
try:
    from dbconfig import dbname, user
except ImportError:
    raise Exception('Need a file called dbconfig.py in same directory as this \
            file, that define the postgres connection variables "dbname" and \
            "user"')

class Acser(object):
    """
    A converter from ambiguous place names to FIPS codes.
    """
    acs3 = 'acs2012_3yr'
    acs1 = 'acs2013_1yr'
    def __init__(self):
        # connect to ACS database
        self.conn = psycopg2.connect('dbname={} user={}'.format(dbname, user))
        self.cur = self.conn.cursor()

        self.col2seq = {x:y for x, y in self.load_all_seqs()}

        return

    def retrieve(self, geo, cols, verbose=False):
        """Return ACS data for given columns
        at the given geo ID.


        """
        # TODO: this method currently depends on a weird denormalized input
        # namely, cols have to be in the format XTTTTT_CCCC, where TTTTT is the
        # "table" number, and CCC is the column number. I think this should be
        # split up into two arguments, perhaps into a "GeoId" object.
        
        tables = {x.split()[0]:[] for x in cols}
        results = {}
        for col in cols:
            table, cspec = col.split('_')
            formatted_column = ''.join((table, cspec)).lower()
            formatted_table = table.lower()

            try:
                seq = self.col2seq[table]
            except KeyError:
                raise ValueError('{} is not a valid ACS column'.format(table))

            results[formatted_column] = self.retrieve_within_table(geo,
                    formatted_table, (formatted_column,), verbose=verbose)

        return results
    
    def retrieve_within_table(self, geo, table, cols, verbose=False, schema=acs3):
        qbase = 'SELECT {q} FROM {schema}.{table} WHERE geoid=%s'
        
        # TODO: need validation on this. way open to injection
        # however, psycopg2 interpolation only works on values, not table or
        # column names
        #
        # we want to interpolate one value per column


        # assert SELECT * FROM information_schema.tables WHERE table_schema='acs2013_1yr';

        query = qbase.format(q='{},'*(len(cols)-1) + '{}',
                schema = schema,
                table = table).format(*cols)
        
        if verbose:
            print(query)
        self.cur.execute(query, (geo,))
        data = self.cur.fetchone()
        
        # return array of single value when only one is returned
        if len(data) == 1:
            data = data[0]

        return data

    def geo_lookup(self, statefp, countyfp, placefp, schema=None):
        """
        look up the census geo_id for a given FIPS code.

        schema is an argument for forcing lookup to happen 
        within a specific schema.
        by default, it will use the acs 3-year geoheaders.

        Note: in the near future, this may change to being
        5-year geoheaders.

        """
        
        qbase = 'SELECT geoid FROM {schema}.geoheader WHERE {p1} AND {p2} AND {p3}'
        
        if not schema:
            schema = self.acs3

        # construct the query and the args:
        args = []

        if statefp:

            p1='state=%s' 
            args.append(statefp)
        else:
            p1='state IS NULL'

        #sometimes a name resolves to both a county and a place
        # in those situations, go with the more specific level,
        # unless otherwise specified
        # TODO: build flag to force level of specificity
        if (countyfp and not placefp):

            p2='county=%s' 
            args.append(countyfp)
        else:
            p2='county IS NULL'

        if placefp:
            p3='place=%s' 
            args.append(placefp)

        else:
            p3='place IS NULL'

        query = qbase.format(schema=schema, p1=p1, p2=p2, p3=p3)
        try:
            self.cur.execute(query, args)
        except (InternalError, ProgrammingError) as e:
            raise ValueError('Invalid query attempted: {}:{}'.format(query, args))
        
        r = self.cur.fetchone()
        if r is None:
            raise ValueError('No geoheader found for {}:{}:{}'.format(
                statefp, countyfp, placefp))
        else:
            gid = r[0]

        return gid
    
    def load_all_seqs(self):
        """might be obsolete with postgres views
        """
        self.cur.execute('SELECT * FROM acs2013_1yr.col2seq')
        return self.cur.fetchall()

    def seq_lookup(self, col):
        """Return sequence code for given column

        might be obsolete

        """
        
        try:
            self.cur.execute('SELECT "Sequence Number" FROM acs2013_1yr.col2seq WHERE "Table ID"=%s', (col,))
        except (InternalError, ProgrammingError) as e:
            raise ValueError('{} is not a valid table.'.format(col))

        seq = self.cur.fetchone()
        if seq is None:
            raise ValueError('{} is not a valid table.'.format(col))
        else:
            ss = 'seq' + seq[0]

        return ss


