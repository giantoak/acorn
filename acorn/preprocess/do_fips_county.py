# coding: utf-8
from fips import FIPSCountyReshaper
import sys

fcr = FIPSCountyReshaper()
fcr.pipeline(sys.stdin, sys.stdout)
