import pandas as pd

DATA_PATH = "data/"

inputs = [
    "part-01.json",
    "part-02.json",
    "part-03.json",
    "part-04.json",
    "part-05.json",
    "part-06.json",
]
netflix = pd.read_csv(DATA_PATH + "netflix_titles.csv")
titles = netflix["title"]

pd.DataFrame().to_csv(DATA_PATH + "out.csv", index=False, mode="w")

for index, file in enumerate(inputs):
    print("Started processing", file)
    reviews = pd.read_json(DATA_PATH + file)

    reviews["movie"].replace(" \([1-9]*.*", "", regex=True, inplace=True)
    reviews = reviews[reviews["movie"].isin(titles)]

    reviews.to_csv(DATA_PATH + "out.csv", index=False, header=(index == 0), mode="a")
    print("Finished processing", file)


print("Finished")
