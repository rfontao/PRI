MIN_RELEASE_YEAR = 2015

# Taken from https://stackoverflow.com/a/3077254/15177524
REVIEWS = data/part-01.json% \
			data/part-02.json% \
			data/part-03.json% \
			data/part-04.json% \
			data/part-05.json% \
			data/part-06.json%

all: data/reviews.csv

data:
	mkdir $@

$(REVIEWS): data
	kaggle datasets download --path data -d ebiswas/imdb-review-dataset
	unzip -n data/imdb-review-dataset.zip -d data

data/netflix_titles.csv: data
	kaggle datasets download --path data -d shivamb/netflix-shows
	unzip -n data/netflix-shows.zip -d data

data/reviews.csv: $(REVIEWS) data/netflix_titles.csv
	python3 reviews.py -y $(MIN_RELEASE_YEAR)
