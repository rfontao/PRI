import pandas as pd
import json

# Process Netflix data to prepare for JSON properties
netflix = pd.read_csv('./data/netflix_titles_clean.csv')

netflix.rename(columns={'listed_in': 'genres', 'director': 'directors', 'country': 'countries'}, inplace=True)

netflix.loc[:, 'date_added'] = pd.to_datetime(netflix['date_added'].str.strip(' '), format='%B %d, %Y')

netflix.loc[:, 'directors'] = netflix['directors'].str.split(', ')
netflix.loc[:, 'cast'] = netflix['cast'].str.split(', ')
netflix.loc[:, 'countries'] = netflix['countries'].str.split(', ')
netflix.loc[:, 'genres'] = netflix['genres'].str.split(', ')

# Process Reviews data to prepare for JSON properties
reviews = pd.read_csv('./data/reviews_clean.csv')

reviews.loc[:, 'review_date'] = pd.to_datetime(reviews['review_date'], format='%d %B %Y')
reviews.loc[:, 'spoiler_tag'] = reviews.loc[:, 'spoiler_tag'].map({0: False, 1: True})

# Merge contents
merged_df = netflix.merge(
    right=reviews.groupby(by=['show_id'])[['review_id', 'reviewer', 'rating', 'review_summary', 'review_date', 'spoiler_tag', 'review_detail', 'total', 'helpful', 'unhelpful']]\
        .apply(lambda x: json.loads(x.to_json(path_or_buf=None, orient='records'))).rename('reviews'),
    how='left',
    on='show_id'   
)

merged_df['avg_rating'] = reviews.groupby(by=['show_id'])['rating'].agg('mean')

# Save final document
merged_df.loc[:,:].to_json(path_or_buf='./data/json/netflix.json', orient='records')