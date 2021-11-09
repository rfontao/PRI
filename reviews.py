import argparse
import pandas as pd


def test(reviews):
    # reviews["date"] = reviews["movie"].str.extract(r" \(([0-9]*).*")
    # reviews["movie"] = reviews["movie"].str.extract(r"(.*) \([0-9]*.*")
    # print(reviews)

    print(reviews["movie"].str.extract(r" \(([0-9]{4}).*")["1500"])


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
netflix = pd.read_csv(DATA_PATH + "netflix_titles.csv")
if args.min_release_year is not None:
    netflix = netflix[netflix["release_year"] > args.min_release_year]

titles = netflix["title"]

pd.DataFrame().to_csv(DATA_PATH + "reviews.csv", index=False, mode="w")

for index, file in enumerate(inputs):
    print("Started processing", file)
    reviews = pd.read_json(DATA_PATH + file)

    print(test(reviews))
    # Remove years at the end of the movies names
    reviews["movie"].replace(r" \([1-9]*.*", "", regex=True, inplace=True)

    # Leave only shows that are on Netflix
    reviews = reviews[reviews["movie"].isin(titles)]

    # Append to the result csv
    reviews.to_csv(DATA_PATH + "reviews.csv", index=False,
                   header=(index == 0), mode="a")
    print("Finished processing", file)


print("Finished")
