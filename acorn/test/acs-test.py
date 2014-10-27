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

from acser import Acser
qs = ["B01001_001","B19013_001","B01001A_001","B01001B_001","B15002_003",
        "B15002_004","B15002_005","B15002_006","B15002_007","B15002_008",
        "B15002_009","B15002_010","B15002_011","B15002_012","B15002_013",
        "B15002_014","B15002_015","B15002_016","B15002_017","B15002_018"]

def test_init():
    a = Acser()
    assert a.conn and a.cur
    assert isinstance(a.col2seq, dict)

def test_retrieve():
    a = Acser()
    def compare(a, g, seqs, ans):
        r = a.retrieve(g, seqs)
        assert r == ans
    
    # kind of a painful test fixture
    tests = ((('04000US51', ['B01001_030', 'B01001_031']), {'b01001030': 152263, 'b01001031': 117142}),
            (('04000US51', ['B01001_030',]), {'b01001030': 152263}),
            (('04000US51', ['B01001_030', 'B01001_031', 'B00001_001', 'B00002_001']), 
                {'b01001030': 152263, 'b01001031': 117142, 'b00001001': 129262,
                    'b00002001': 52452}),
            )

    for (g, seqs), ans in tests:
        yield compare, a, g, seqs, ans

def test_retrieve_within_table():
    a = Acser()
    def compare(a, g, table, cols, ans):
        r = a.retrieve_within_table(g, table, cols)
        assert r == ans
    
    tests = ((('04000US51', 'seq0002', ['b01001030', 'b01001031']), (152263, 117142)),
            (('04000US51', 'seq0002', ['b01001030',]), 152263),
            )
    for (g, seq, cols), ans in tests:
        yield compare, a, g, seq, cols, ans

def test_geoid():
    a = Acser()
    def compare(a, s, c, g, gid):
        r = a.geo_lookup(s, c, p)
        assert r == gid

    tests = {('51', None, None): '04000US51',
            ('02', None, '03000'): '16000US0203000',
            }

    for (s, c, p), gid in tests.iteritems():
        yield compare, a, s, c, p, gid

def test_geoid_fail():
    @raises(ValueError)
    def fails(a, s, c, g):
        geo = a.geo_lookup(s, c, g)
        print geo

    a = Acser()
    tests = (
            # Turns out, neither of these raise exceptions: rather they retrieve all 
            # the records from Puerto Rico:
            #(None, None, None),
            #(0, 0 ,0),
            ('02', None, '012345'),
            ('a', '$$$$', 'kk12kj123oi213'))

    for s, c, g in tests:
        yield fails, a, s, c, g

def test_seq_lookup():
    def compare(a, table, ans):
        seq = a.seq_lookup(table)
        assert seq == ans

    a = Acser()
    tests = {'B01001': 'seq0002'}

    for t, s in tests.iteritems():
        yield compare, a, t, s

def test_seq_lookup_fail():
    @raises(ValueError)
    def compare(a, table):
        seq = a.seq_lookup(table)
        assert True
    
    a = Acser()
    tests = ['', 1, None, 'BKDFKMW@:']

    for t in tests:
        yield compare, a, t
