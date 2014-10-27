# coding: utf-8
import nose
import os
import sys
import numpy as np
from nose.tools import *

path = os.path.dirname(
        os.path.dirname(
            os.path.realpath(__file__)))
sys.path.append(os.path.join(path, 'retrieval'))

from fetcher import ApiFetcher

tbs = ["B01001_001","B19013_001","B01001A_001","B01001B_001","B15002_003",
        "B15002_004","B15002_005","B15002_006","B15002_007","B15002_008",
        "B15002_009","B15002_010","B15002_011","B15002_012","B15002_013",
        "B15002_014","B15002_015","B15002_016","B15002_017","B15002_018"]

gids = ['04000US51', '04000US51', '16000US0203000', '16000US0203000', '16000US5136648']

def test_tokenize():
    a = ApiFetcher()

    assert a.tokenize('B01001_001') == {'table': 'B01001', 'col': 'B01001001'}

def test_retrieve():
    a = ApiFetcher()
    
    js = a.get(tbs, gids)

