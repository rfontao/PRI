import pandas as pd
from pandas.core import series

titles = pd.read_csv('data/netflix_titles.csv')

# Convert show_id to int, then set as index
titles.loc[:, 'show_id'] = titles['show_id'].str.replace('s', '').astype(int)
titles.set_index('show_id', inplace=True)

# Fix columns in wrong order
idx = titles['duration'].isnull()
titles.loc[idx, 'duration'] = titles['rating']
titles.loc[idx, 'rating'] = 'NR'

# Fix missing values in rating
titles.loc[titles['rating'].isnull(), 'rating'] = 'NR'
titles.loc[titles['rating'] == 'UR', 'rating'] = 'NR'

# Fix incorrect list formatting
titles.loc[:, 'country'] = titles.loc[:, 'country'].str.lstrip(to_strip=', ')

# Remove 'min' from movie durations and 'Season' / 'Seasons' from tv shows
movies = titles['type']=='Movie'
shows = titles['type']=='TV Show'

titles.loc[movies, 'duration'] = titles.loc[movies, 'duration'].str.rstrip('min ')
titles.loc[shows, 'duration'] = titles.loc[shows, 'duration'].str.rstrip('Seasons ')

titles['duration'].astype(int)


titles.to_csv('data/netflix_titles_clean.csv')
