.PHONY: all
all: data/reviews_clean.csv data/netflix_titles_clean.csv

data:
	mkdir $@

data/netflix-shows.zip: data
	kaggle datasets download --path data -d shivamb/netflix-shows
	touch data/netflix-shows.zip

data/netflix_titles.csv: data/netflix-shows.zip
	unzip -n data/netflix-shows.zip -d data
	touch $@

data/imdb-review-dataset.zip: data
	kaggle datasets download --path data -d ebiswas/imdb-review-dataset
	touch $@

data/reviews.csv: data/imdb-review-dataset.zip data/netflix_titles.csv reviews.py
	unzip -n data/imdb-review-dataset.zip -d data
	python3 reviews.py


data/reviews_clean.csv: data/reviews.csv
	cp data/reviews.csv data/reviews_clean.csv

data/netflix_titles_clean.csv: data/netflix_titles.csv cleanup.py
	python3 cleanup.py


.PHONY: cleanjson
cleanjson:
	rm -f data/*.json

.PHONY: cleanlocal
cleanlocal:
	rm -f data/*.json data/*.csv

