import sys
import pandas as pd

burn_list = ['city', 'CDP', 'town', 'township', 'village', 'borough', 'comunidad',
        'UT', 'defined', 'urbana', 'plantation', 'Reservation', 'grant', '(balance)',
        'municipality', 'purchase', 'location', 'gore', 'government', 'County',
        'corporation', '157-30', 'City', '158-30', 'county']


def remove_census_suffixes(loc):
    parts = [x.strip() for x in loc.split(' ')]
    
    if len(parts) == 1:
        return parts[0]

    # remove all parts from the end of place name that is in the burn_list
    for i in range(len(parts)-1, -1, -1):
        if parts[i] not in burn_list:
            break

    name = ' '.join(parts[:i+1])

    return name

def clean_fips(col, outcol):
    # clean fips place
    df_place = pd.read_csv(sys.stdin)
    df_place[outcol] = df_place[col].apply(remove_census_suffixes)
    df_place.to_csv(sys.stdout, index=False)

if __name__ == '__main__':
    clean_fips(sys.argv[1], sys.argv[2])
