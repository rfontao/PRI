import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--min_release_year', '-y', type=int,
                    help='Minimum release year of Netflix show')

args = parser.parse_args()

netflix = pd.read_csv('data/netflix_titles.csv')

# Convert show_id to int, then set as index
netflix.loc[:, 'show_id'] = netflix['show_id'].str.replace('s', '').astype(int)
netflix.set_index('show_id', inplace=True)

# Filter only most recent shows
if args.min_release_year is not None:
    netflix = netflix.loc[netflix['release_year'] > args.min_release_year]

# Fix columns in wrong order
idx = netflix['duration'].isnull()
netflix.loc[idx, 'duration'] = netflix['rating']
netflix.loc[idx, 'rating'] = 'TV-MA' # Manually verified

# Manually verified ratings
netflix.loc[7538, 'rating'] = 'TV-14'
netflix.loc[7313, 'rating'] = 'TV-MA'
netflix.loc[7538, 'rating'] = 'PG-13'
netflix.loc[8791, 'rating'] = 'PG-13'

# Fix missing values in rating
netflix.loc[netflix['rating'].isnull(), 'rating'] = 'NR'
netflix.loc[netflix['rating'] == 'UR', 'rating'] = 'NR'

# Fix incorrect list formatting
netflix.loc[:, 'country'] = netflix.loc[:, 'country'].str.lstrip(to_strip=', ')

# Remove 'min' from movie durations and 'Season' / 'Seasons' from tv shows
movies = netflix['type']=='Movie'
shows = netflix['type']=='TV Show'

netflix.loc[movies, 'duration'] = netflix.loc[movies, 'duration'].str.rstrip('min ')
netflix.loc[shows, 'duration'] = netflix.loc[shows, 'duration'].str.rstrip('Seasons ')

netflix['duration'].astype(int)

netflix.to_csv('data/netflix_titles_clean.csv')
