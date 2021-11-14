import argparse
import pandas as pd

DATA_PATH = "data/"

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--min_release_year', '-y', type=int,
                    help='Minimum release year of Netflix series')

args = parser.parse_args()

inputs = [
    "part-01.json",
    "part-02.json",
    "part-03.json",
    "part-04.json",
    "part-05.json",
    "part-06.json",
]

netflix = pd.read_csv('data/netflix_titles_clean.csv')
netflix.rename(columns={'rating': 'audience_rating'}, inplace=True)

# Filter only most recent shows
if args.min_release_year is not None:
    netflix = netflix[netflix["release_year"] > args.min_release_year]

pd.DataFrame().to_csv(DATA_PATH + "reviews.csv", index=False, mode="w")

for index, file in enumerate(inputs):
    print(f'[{index+1}/{len(inputs)}] Processing {file}  ...  ', end='', flush=True)
    reviews = pd.read_json(DATA_PATH + file)

    # Remove years at the end of the movies names
    reviews["movie"].replace(" \([1-9]*.*", "", regex=True, inplace=True)

    # Merge to filter shows that are not on Netlix and add the respective show_id
    filtered = pd.merge(reviews, netflix, left_on=['movie'], right_on=['title'], how='inner')

    cols_to_del = list(netflix.columns)
    cols_to_del.remove('show_id')

    filtered.drop(columns=cols_to_del, inplace=True)

    # Append to the result csv
    filtered.to_csv(DATA_PATH + "reviews.csv", index=False,
                   header=(index == 0), mode="a")

    print("Finished")
