import pandas as pd

burn_list = ['city', 'CDP', 'town', 'township', 'village', 'borough', 'comunidad',
        'UT', 'defined', 'urbana', 'plantation', 'Reservation', 'grant', '(balance)',
        'municipality', 'purchase', 'location', 'gore', 'government', 'County',
        'corporation', '157-30', 'City', '158-30', 'county']

df = pd.read_csv('regions.csv')

def strip_census_suffixes(loc):
    """ remove all suffixes in a loc string, such that a place like
    Indianapolis City (balance) becomes Indianapolis
    """

    parts = loc.split(',')

df2 = df.copy()

df2['loc_parts'] = df.location.apply(lambda x: x.split(','))

df['loc'] = df2['loc_parts'].apply(lambda x: ','.join(x[:-1]))
df = df[df2['loc_parts'].apply(lambda x: x[-1].strip()) == 'USA']\
        .drop('location', 1)

df.to_csv('locations.csv', index=False)
