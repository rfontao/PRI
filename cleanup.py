import pandas as pd

titles = pd.read_csv('netflix_titles.csv')

titles[titles['duration'].isnull()].rename(columns={'rating':'duration','duration':'rating'})


