#!/bin/bash

cat data/fips_states.csv \
	| pit -d, -e 'print _[0] + "," + _[1].lower()' \
	> data/fips_states_lower.csv

cat data/states.csv \
	| pit -e 'print _.lower()' \
	> data/states_lower.csv

csvjoin -c state data/fips_states_lower.csv data/states_lower.csv \
	| csvcut -c 1,2,4 \
	> data/fips_states_all.csv

#cat data/fips_county2.csv | pit '_.lower()' > data/fips_county3.csv
cat data/fips_place.csv \
	| pit -e 'print _.lower()' \
	| pit -f 'not _.startswith("pr")'\
	| utils/csvpad 'statefp' 2 \
	| utils/csvpad 'placefp' 5 \
	> data/fips_place_final.csv
	#| iconv -f ISO8859-2 -t UTF-8 -o data/fips_place_lower.csv

# make a denormalized table mapping place fips to county fips
cat data/fips_place_final.csv \
	| python preprocess/normalize_place_counties.py \
	> data/place2counties.csv

# rename the column headers to be more consistent across files
# countyfp --> 3-digit county fips
# statefp --> 2-digit state fips
# placefp --> 5-digit place fips
# fips --> agglomerated fips code (not necessarily standardized)
cat data/fips_county2.csv \
	| utils/csvrename county_fips:countyfp \
				state_fips:statefp \
	> data/fips_county_final.csv

cat data/fips_states_all.csv \
	| utils/csvrename fips:statefp \
	> data/fips_state_final.csv

# make mapping from acs table names to sequence numbers
cat data/acs_col_seq_metadata.csv \
	| csvcut -e iso-8859-2 -c 2,3 \
	| uniq \
	> data/acs_col2seq.csv

# insert tables into the database
# drop existing tables
psql -U sam acs_2013 -c "DROP TABLE IF EXISTS acs2013_1yr.place2counties"
csvsql --db postgresql:///acs_2013 \
	--db-schema acs2013_1yr \
	--table place2counties \
	--insert data/place2counties.csv 

psql -U sam acs_2013 -c "DROP TABLE IF EXISTS acs2013_1yr.name2placefp"
csvsql -e iso-8859-2 \
	--db postgresql:///acs_2013 \
	--db-schema acs2013_1yr \
	--table name2placefp \
	--insert data/fips_place_final.csv

psql -U sam acs_2013 -c "DROP TABLE IF EXISTS acs2013_1yr.name2countyfp"
csvsql --db postgresql:///acs_2013 \
	--db-schema acs2013_1yr \
	--table name2countyfp \
	--insert data/fips_county_final.csv

psql -U sam acs_2013 -c "DROP TABLE IF EXISTS acs2013_1yr.name2statefp"
csvsql --db postgresql:///acs_2013 \
	--db-schema acs2013_1yr \
	--table name2statefp \
	--insert data/fips_states_all.csv

psql -U sam acs_2013 -c "DROP TABLE IF EXISTS acs2013_1yr.col2seq"
csvsql 	-e iso-8859-2 \
	--db postgresql:///acs_2013 \
	--db-schema acs2013_1yr \
	--table col2seq \
	--insert data/acs_col2seq.csv


python retrieval/tag_bp.py > data/bp_acs.csv
