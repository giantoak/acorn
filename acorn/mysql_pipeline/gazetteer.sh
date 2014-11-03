#!/bin/bash
# an end-to-end pipeline for loading census gazetteer data into a mysql database

source mysql_pipeline/mysqlconfig.sh

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

echo $dburl

csvsql --db $dburl \
    --query "DROP DATABASE IF EXISTS census; CREATE DATABASE IF NOT EXISTS census"

csvsql --db $dburl \
    --db-schema census\
    --table gaz_places \
    --insert data/gaz_place.csv

csvsql --db $dburl \
    --db-schema census \
    --table gaz_counties \
    --insert data/gaz_county.csv






