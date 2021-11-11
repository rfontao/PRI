import pandas as pd

reviews = pd.read_csv('data/reviews.csv')

# Convert show_id to int, then set as index
reviews.loc[:, 'review_id'] = reviews['review_id'].str.replace('rw', '').astype(int)
reviews.set_index('review_id', inplace=True)

reviews.to_csv('data/reviews_clean.csv')
