#!/bin/bash

cat data/region_level_all.csv \
    | python retrieval/geo_lookup.py \
    > data/region_level_geocoded.csv

csvjoin -v -c gid \
    data/crime2013_tagged_clean.csv \
    data/region_level_geocoded.csv \
    > data/region_level_acs_crime.csv

