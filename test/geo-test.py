import pandas as pd
import sys
import os
from nose.tools import *

dirroot = os.path.dirname(
            os.path.dirname(
                os.path.realpath(__file__)))

sys.path.extend([os.path.join(dirroot, 'retrieval'),
    os.path.join(dirroot, 'preprocess')])

from acser import Acser
from geoider import Geoider


def test_lookup():
    acs = Acser()

    def succeeds(statefp, countyfp, placefp, schema, geo):
        g = acs.geo_lookup(statefp, countyfp, placefp)
        assert g==geo
    
    @raises(ValueError)
    def fails(statefp, countyfp, placefp, schema, geo):
        g = acs.geo_lookup(statefp, countyfp, placefp, schema)
        assert g==geo
    
    success_tests = {('51', None, None, 'acs2013_1yr'): '04000US51',
                    ('51', None, None, None): '04000US51',
                    ('02', None, '03000', 'acs2013_1yr'): '16000US0203000',
                    ('02', None, '03000', None): '16000US0203000',
                    ('51', None, '36648', None): '16000US5136648',
                    }
    
    fail_tests = {
            # Herndon, VA --> Population 23,292
            ('51', None, '36648', 'acs2013_1yr'): '16000US5136648',
            }
    for (s, c, p, sch), g in success_tests.iteritems():
        yield succeeds, s, c, p, sch, g

    for (s, c, p, sch), g in fail_tests.iteritems():
        yield fails, s, c, p, sch, g
    

