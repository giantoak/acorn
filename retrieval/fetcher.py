#!/bin/python
import requests

class ApiFetcher(object):
    show_base = 'http://api.censusreporter.org/1.0/data/show/latest?table_ids={tbs}&geo_ids={gs}'
    
    def __init__(self):
        return
    
    def tokenize(self, col):
        """Takes column name and tokenizes into table, table + col.
        
        Currently expecteds column names to be table_col"""

        table, col = col.strip().upper().split('_')
        col = table + col

        return {'table': table, 'col': col}

    def get(self, tables, geos):
        tokens = [self.tokenize(x) for x in tables]
        tbs = ','.join([x['table'] for x in tokens])
        gs = ','.join(geos)

        r = requests.get(self.show_base.format(tbs=tbs, gs=gs))


        if not r.ok:
            raise ValueError(r.text)

        js = r.json()
        return js

