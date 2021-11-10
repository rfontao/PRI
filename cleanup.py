import pandas as pd

titles = pd.read_csv('data/netflix_titles.csv')

# Fix columns in wrong order
idx = titles['duration'].isnull()
titles.loc[idx, 'duration'] = titles['rating']
titles.loc[idx, 'rating'] = 'NR'

# Fix missing values in rating
titles.loc[titles['rating'].isnull(), 'rating'] = 'NR'
titles.loc[titles['rating'] == 'UR', 'rating'] = 'NR'

# Fix incorrect list formatting
titles.loc[:, 'country'] = titles.loc[:, 'country'].str.lstrip(to_strip=', ')

titles.to_csv('data/netflix_titles_clean.csv')
