#!/bin/bash

cat data/crime_scrape2013_fullnames.csv | python retrieval/acorn_doc.py full_name > data/crime2013_tagged.csv

cat data/crime2013_tagged.csv | python utils/csviffuniq 'gid' > data/crime2013_tagged_clean.csv
