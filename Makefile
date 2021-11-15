MIN_SHOW_YEAR:=1200

.PHONY: all
all: data/reviews_clean.csv data/netflix_titles_clean.csv images/.plots

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


data/netflix_titles_clean.csv: data/netflix_titles.csv scripts/cleanup_netflix.py
	python3 scripts/cleanup_netflix.py -y $(MIN_SHOW_YEAR)


data/reviews.csv: data/imdb-review-dataset.zip data/netflix_titles_clean.csv scripts/filter_reviews.py
	unzip -n data/imdb-review-dataset.zip -d data
	python3 scripts/filter_reviews.py

data/reviews_clean.csv: data/reviews.csv scripts/cleanup_reviews.py
	python3 scripts/cleanup_reviews.py

images:
	mkdir $@

images/.plots: images data/netflix_titles_clean.csv data/reviews_clean.csv scripts/gen_plots.py
	python3 scripts/gen_plots.py
	touch images/.plots


.PHONY: cleanjson
cleanjson:
	rm -f data/*.json

.PHONY: cleanlocal
cleanlocal:
	rm -f data/*.json data/*.csv

