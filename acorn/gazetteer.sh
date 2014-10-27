#!/bin/bash
# an end-to-end pipeline for loading census gazeteer data into a postgres database


# convert census gazetteer file into proper shape
cat data/2014_Gaz_place_national.txt \
    | utils/csvresep '\t' , \
    | utils/csvrename NAME:PLACENAME \
    | python preprocess/strip_census_suffix.py PLACENAME NAME ','\
    | pit -e 'print _.lower()' \
    | pit -f 'not _.startswith("pr")' \
    | utils/csvpad geoid 7 \
    > data/gaz_place_lower.csv

# join with state fips
csvjoin -e iso-8859-2 \
        -c usps,abbreviation \
        data/gaz_place_lower.csv \
        data/fips_states_all.csv \
    | csvcut -C abbreviation,state \
    | utils/csvrename fips:statefp \
    > data/gaz_place.csv

# preprocess national gazetteer data
cat data/2014_Gaz_counties_national.txt \
    | utils/csvresep '\t' , \
    | utils/csvrename NAME:COUNTY \
    | pit -e 'print _.lower()' \
    | python preprocess/do_fips_county.py \
    | utils/csvpad geoid 7 \
    > data/gaz_county_lower.csv

# join national gazetteer data with state fips
csvjoin -e iso-8859-2 \
        -c usps,abbreviation \
        data/gaz_county_lower.csv \
        data/fips_states_all.csv \
    | csvcut -C abbreviation,state \
    | utils/csvrename fips:statefp \
    > data/gaz_county.csv

psql -U sam acorn -c "DROP SCHEMA IF EXISTS gaz CASCADE"
psql -U sam acorn -c "CREATE SCHEMA IF NOT EXISTS gaz"

csvsql --db postgresql:///acorn \
    --db-schema gaz \
    --table places \
    --insert data/gaz_place.csv

csvsql --db postgresql:///acorn \
    --db-schema gaz \
    --table counties \
    --insert data/gaz_county.csv








