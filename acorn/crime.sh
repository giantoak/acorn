#!/bin/bash

cat data/crime_scrape2013_fullnames.csv \
    | python retrieval/acorn_doc.py full_name \
    > data/crime2013_tagged.csv

cat data/crime2013_tagged.csv \
    | python utils/csviffuniq 'gid' \
    > data/crime2013_tagged_clean.csv


psql -U sam acorn -c "DROP SCHEMA EXISTS crime13"
psql -U sam acorn -c "CREATE SCHEMA IF NOT EXISTS crime13"
psql -U sam acorn -c "DROP TABLE IF EXISTS crime13.*"

csvsql --db postgresql:///acorn \
    --db-schema crime13 \
    --table precinct \
    --insert data/crime2013_tagged_clean.csv
