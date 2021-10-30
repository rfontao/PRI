all: cull-reviews

data:
	mkdir $@

reviews: data
	kaggle datasets download --path data -d ebiswas/imdb-review-dataset --unzip

netflix: data
	kaggle datasets download --path data -d shivamb/netflix-shows --unzip

cull-reviews: reviews netflix
	python3 reviews.py
