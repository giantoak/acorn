#!/bin/bash

# an end-to-end pipeline for transforming data into a postgres database

# certain things need to be made lowercased for consistency
cat data/fips_states.csv \
	| pit -d, -e 'print _[0] + "," + _[1].lower()' \
	> data/fips_states_lower.csv

cat data/states.csv \
	| pit -e 'print _.lower()' \
	> data/states_lower.csv

csvjoin -c state data/fips_states_lower.csv data/states_lower.csv \
	| csvcut -c 1,2,4 \
	> data/fips_states_all.csv

# unfortunately, a preprocessing step was lost. the original fips_place.csv file
# was downloaded from the census site, and was pipe delimited. I added a column called
# PLACENAME which is wrong. So it is done correctly here:
cat data/fips_place.csv \
	| csvcut -e iso-8859-2 -C NAME,SUFFIX \
	| python preprocess/strip_census_suffix.py PLACENAME NAME ',' \
	> data/fips_place_name.csv

#cat data/fips_county2.csv | pit '_.lower()' > data/fips_county3.csv
cat data/fips_place_name.csv \
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

# rename files to follow convention (statefp = state fips, 
# 				countyfp=county fips, etc)

cat data/fips_states_all.csv \
	| utils/csvrename fips:statefp \
	> data/fips_state_final.csv

# make mapping from acs table names to sequence numbers
cat data/acs_col_seq_metadata.csv \
	| csvcut -e iso-8859-2 -c 2,3 \
	| uniq \
	> data/acs_col2seq.csv

# insert tables into the database
# TODO: make the postgres credentials not hardcoded

psql -U sam acorn -c "DROP SCHEMA IF EXISTS mappings CASCADE"
psql -U sam acorn -c "CREATE SCHEMA IF NOT EXISTS mappings"
csvsql --db postgresql:///acorn \
	--db-schema mappings \
	--table place2counties \
	--insert data/place2counties.csv 

csvsql -e iso-8859-2 \
	--db postgresql:///acorn \
	--db-schema mappings \
	--table name2placefp \
	--insert data/fips_place_final.csv

csvsql --db postgresql:///acorn \
	--db-schema mappings \
	--table name2countyfp \
	--insert data/fips_county_final.csv

csvsql --db postgresql:///acorn \
	--db-schema mappings \
	--table name2statefp \
	--insert data/fips_states_all.csv

csvsql 	-e iso-8859-2 \
	--db postgresql:///acorn \
	--db-schema mappings \
	--table col2seq \
	--insert data/acs_col2seq.csv

# tag backpage places with geo_ids
python retrieval/tag_bp.py > data/bp_acs.csv

# generate place names that don't fulfill criteria:
cat data/locations_resolved.csv | pit -d , -f 'not _[0] and not _[1]' | pit -d , -e 'print "\"%s\""%_[3]' > data/bp_mappings.csv 


# run crime preprocessing
#./crime.sh
