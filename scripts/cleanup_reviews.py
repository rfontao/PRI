import pandas as pd

reviews = pd.read_csv('data/reviews.csv')

# Convert show_id to int, then set as index
reviews.loc[:, 'review_id'] = reviews['review_id'].str.replace('rw', '').astype(int)
reviews.set_index('review_id', inplace=True)

# Remove null review summaries
reviews = reviews[~(reviews['review_summary'].isnull())]

# Separate helpful list column
reviews.rename(columns={'helpful': 'helpful_list'}, inplace=True)
temp = reviews.loc[:, 'helpful_list'].str.strip('[]').str.replace('\'|,', '', regex=True).str.split(' ')

reviews.loc[:, ['total']] = temp.apply(lambda x: x[1]).astype(int)
reviews.loc[:, ['helpful']] = temp.apply(lambda x: x[0]).astype(int)

reviews['unhelpful'] = reviews['total'] - reviews['helpful']

reviews.drop('helpful_list', axis=1, inplace=True)

# Write new clean dataset
reviews.to_csv('data/reviews_clean.csv')
