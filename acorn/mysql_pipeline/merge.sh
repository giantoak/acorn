#!/bin/bash

cat data/region_level_all.csv \
    | csvcut -C state_fips,county_fips,place_fips \
    | python retrieval/acorn_doc.py place state \
    > data/region_level_geocoded.csv

csvjoin -v -c gid \
    data/crime2013_tagged_clean.csv \
    data/region_level_geocoded.csv \
    | csvcut -C 23,58,59\
    > data/region_level_acs_crime.csv

