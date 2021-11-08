all: data/reviews.csv

data:
	mkdir $@

reviews: data
	kaggle datasets download --path data -d ebiswas/imdb-review-dataset
	unzip -n data/imdb-review-dataset.zip -d data

netflix: data
	kaggle datasets download --path data -d shivamb/netflix-shows
	unzip -n data/netflix-shows.zip -d data

data/reviews.csv: reviews netflix
	python3 reviews.py
