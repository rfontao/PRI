import pandas as pd

titles = pd.read_csv('data/netflix_titles.csv')

titles[titles['duration'].isnull()].rename(columns={'rating':'duration','duration':'rating'})

titles.to_csv('data/netflix_titles_clean.csv')
