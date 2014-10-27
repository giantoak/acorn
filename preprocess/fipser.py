from __future__ import print_function
import pandas as pd
import sys
import os
import re

class Fipser(object):
    """
    A converter from ambiguous place names to FIPS codes.
    """
    def __init__(self):
        path = os.path.dirname(
                os.path.dirname(
                    os.path.realpath(__file__)))

        datadir = os.path.join(path, 'data')
    
        # the index column of a dataframe is hashed for O(1) access
        # however, only one index can exist per column (as of these
        # humble times in September 2014)

        # to speed up retrieval, we create separate dataframes
        # for each column that we need indexed
        
        # TODO: replace this with database accesses
        # TODO: use gazetteer data
        self.county = pd.read_csv(os.path.join(datadir, 'fips_county_final.csv'), 
                index_col='county_name', dtype=object)
        self.county_full_name_idx = self.county.copy()
        self.county_full_name_idx.set_index('county', inplace=True)

        self.place = pd.read_csv(os.path.join(datadir, 'fips_place_final.csv'),
                index_col='name', dtype=object)
        self.place_full_name_idx = self.place.copy()
        self.place_full_name_idx.set_index('placename', inplace=True)
        
        self.states = pd.read_csv(os.path.join(datadir, 'fips_state_final.csv'),
                index_col='abbreviation', dtype=object)
        self.states_full_name_idx = self.states.copy()
        self.states_full_name_idx.set_index('state', inplace=True)
        
        return

    def resolve(self, location, verbose=False):
        """Return FIPS code at multiple levels of specificity for location.

        """
        def filt_func(s):
            # filter empty strings and commas
            return len(s.strip()) and s.strip() != ','

        parts_raw = re.split(r'([^, ]+)', location.lower())
        parts = [x.strip() for x in filter(filt_func, parts_raw)]

        # i is index for the place name (place/county)
        # j is the index for the state name
        # k is the index for the zip code
        # i <= j <= k
        
        # for each pass, the number of filled in parts in the fips code is
        results = {}

        # move a sliding index across the partitions
        # choose the split that produces both a state and a local FIPS
        # if no split exists, bias towards the more general case
        for i in range(0, len(parts)+1):
            for z in range(len(parts)-1, len(parts)+1):

                # first, try to resolve each of the segments into fips codes
                place_candidate = ' '.join(parts[0:i])
                state_candidate = ' '.join(parts[i:z])
                zip_candidate = parts[z:len(parts)]
                
                
                sfips = self._resolve_part('state', state_candidate)
                pfips = self._resolve_part('place', place_candidate, sfips)
                cfips = self._resolve_part('county', place_candidate, sfips)
                
                # note: place and county are attempts at resolving the same
                # entity across different spatial levels. for this purpose,
                # we are going to resolve it toward the larger area by default

                # for deciding the optimal split, we create a score for each split:
                # the split gets one point for resolving a state, and one point
                # for resolving either place or county (but only one point for both).

                # ties for one point are resolved by picking the split that resolved
                # the higher-level area.
                score = 0
                score += (sfips is not None)
                score += ((pfips is not None) or (cfips is not None))
                
                ans = {
                        'state_fips': sfips,
                        'place_fips': pfips,
                        'county_fips': cfips,
                        'score': score,
                        }
                if verbose:
                    print(i, z, '*{}*{}*'.format(place_candidate, state_candidate))
                    print(ans)

                results[(i, z)] = ans

                # no ties for two points should arise
        
        # get max from results
        # return the winner.
        df = pd.DataFrame(results).T

        max_score = df['score'].max()
        # if the split resolved both state and place, then select that candidate
        if max_score == 2:
            result = df[df['score'] == max_score].drop('score', 1).T.to_dict()\
                    .values()[0]
        
        # TODO: refactor out some of this repetitive stuff into a method
        elif max_score == 1:
            # if the split only resolved one, first try to select the candidate that 
            # did state
            cands = df[df['score'] == max_score].drop('score', 1)
            
            raw = cands[~cands['state_fips'].isnull()].T.to_dict()
            if not len(raw):
                raw = cands[~cands['county_fips'].isnull()].T.to_dict()
            if not len(raw):
                raw = cands.T.to_dict()

            result = raw.values()[0]

        
        # no candidates were chosen
        else:
            result = {
                        'state_fips': None,
                        'place_fips': None,
                        'county_fips': None,
                    }
        
        return result

        # get the candidates by 1) finding all the max scores
    
    def _resolve_part(self, level, name, precursor=None):
        """
        name: state, county, or place name
        level: 'state', 'county', or 'place'
        precursor: fips code of previously ascertained state, if any
        
        """
        
        #TODO:: standardize column names across files
        if level == 'state':
            use_dfs = [self.states, self.states_full_name_idx]
            use_fp = 'statefp'
        elif level == 'county':
            use_dfs = [self.county, self.county_full_name_idx]
            use_fp = 'countyfp'
        elif level == 'place':
            use_dfs = [self.place, self.place_full_name_idx]
            use_fp = 'placefp'
        else:
            # invalid fp
            raise ValueError('Invalid level: {}\n\
                    Valid levels are "state", "county", and "place"'
                    .format(level))

        result = None
        for df in use_dfs:

            if precursor:
                df = df[df['statefp'] == precursor]

            try:
                result = df.ix[name.lower(), use_fp]
                # grab first result to break ties
                if not isinstance(result, basestring):
                    result = result.iloc[0]

            except (ValueError, KeyError, IndexError) as e:
                pass
            
            # only attempt backup dataframe if first didn't
            # return anything
            if result is not None:
                break

        return result

    def score(self, f, place_col):

        df = pd.read_csv(f)

        resolved = []
        for i, row in df.iterrows():
            query = row[place_col]
            ans = self.resolve(query)
            resolved.append(ans)

        df_results = pd.DataFrame(list(resolved)) 
        df_results = pd.concat([df_results, df], axis=1)

        df_results.to_csv('data/{}.out'.format(f), index=False)

if __name__ == '__main__':
    f = Fipser()
    f.score(sys.argv[1], sys.argv[2])
