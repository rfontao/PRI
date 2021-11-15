import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import regex


plt.style.use('netflix.mplstyle')
palette = {'primary': '#221f1f', 'secondary': '#b20710', 'accent': '#e50914', 'tertiary': '#f5f5f1'}

reviews = pd.read_csv('data/reviews_clean.csv', index_col='review_id')
reviews.head()

netflix = pd.read_csv('data/netflix_titles_clean.csv', index_col='show_id')
netflix.head()

movies = netflix[netflix['type']=='Movie']
shows = netflix[netflix['type']=='TV Show']

# ----------------------------
#       NETFLIX DATA
# ----------------------------

def maturity_rating_distribution():
    fig, ax = plt.subplots()
    movies['rating'].value_counts().plot(kind='bar', ax=ax, alpha=0.75, color=palette['secondary'], label='Movies')
    shows['rating'].value_counts().plot(kind='bar', ax=ax, label='TV Shows')

    ax.set_title('Titles by maturity rating')
    ax.set_xlabel('Maturity rating')
    ax.set_ylabel('Count')

    ax.bar_label(ax.containers[0])
    ax.bar_label(ax.containers[1], color=palette['tertiary'])

    ax.legend()

    plt.savefig('images/svg/maturity_rating_distribution.svg', format="svg")
    plt.savefig('images/png/maturity_rating_distribution.png', format="png", dpi=150, bbox_inches="tight")
maturity_rating_distribution()


def genre_distribution():
    genre_count_tv = dict()
    genre_count_movie = dict()

    for _, value in movies['listed_in'].iteritems():
        for genre in value.split(', '):
            genre_count_movie[genre] = genre_count_movie.get(genre, 0) + 1

    for _, value in shows['listed_in'].iteritems():
        for genre in value.split(', '):
            genre_count_tv[genre] = genre_count_tv.get(genre, 0) + 1

    genre_tv = pd.Series(genre_count_tv)
    genre_movie = pd.Series(genre_count_movie)

    fig, axs = plt.subplots(1, 2, figsize=(12, 4))
    ax1, ax2 = axs

    genre_tv.sort_values(ascending=False).plot(kind='bar', ax=ax2, color=palette['secondary'])
    ax2.set_title('Genre distribution on TV shows')
    ax2.set_xlabel('Genres')
    ax2.set_ylabel('Count')

    genre_movie.sort_values(ascending=False).plot(kind='bar', ax=ax1, color=palette['secondary'])
    ax1.set_title('Genre distribution on Movies')
    ax1.set_xlabel('Genres')
    ax1.set_ylabel('Count')

    for container in ax1.containers:
        ax1.bar_label(container)
    for container in ax2.containers:
        ax2.bar_label(container)

    plt.savefig('images/svg/genre_distribution.svg', format="svg")
    plt.savefig('images/png/genre_distribution.png', format="png", dpi=150, bbox_inches="tight")
genre_distribution()


def country_distribution():
    country_count_tv = dict()
    country_count_movie =  dict()

    filtered_movies = movies['country'][movies['country'].notnull()]
    filtered_tv = shows['country'][shows['country'].notnull()]

    for _, value in filtered_movies.iteritems():
        if value:
            for country in value.split(', '):
                country_count_movie[country] = country_count_movie.get(country, 0) + 1

    for _, value in filtered_tv.iteritems():
        if value:
            for country in value.split(', '):
                country_count_tv[country] = country_count_tv.get(country, 0) + 1

    country_tv = pd.Series(country_count_tv)
    country_movie = pd.Series(country_count_movie)

    fig, axs = plt.subplots(1, 2, figsize=(12, 4))
    ax1, ax2 = axs

    country_tv.nlargest(20).plot(kind='bar', ax=ax2, color=palette['secondary'])
    ax2.set_title('Top 20 most frequent countries on TV shows')
    ax2.set_xlabel('Countries')
    ax2.set_ylabel('Count')

    country_movie.nlargest(20).plot(kind='bar', ax=ax1, color=palette['secondary'])
    ax1.set_title('Top 20 most frequent countries on Movies')
    ax1.set_xlabel('Countries')
    ax1.set_ylabel('Count')

    for container in ax1.containers:
        ax1.bar_label(container)
    for container in ax2.containers:
        ax2.bar_label(container)

    plt.savefig('images/svg/country_distribution.svg', format="svg")
    plt.savefig('images/png/country_distribution.png', format="png", dpi=150, bbox_inches="tight")
country_distribution()


def duration_distribution():
    fig, axs = plt.subplots(1, 2, figsize=(12, 4))
    ax1, ax2 = axs

    sns.histplot(movies['duration'], bins=20, ax=ax1, kde=True, color=palette['secondary'])
    ax1.set_title('Movies by duration')
    ax1.set_xlabel('Duration (min)')

    shows.groupby('duration').count()['title'].plot(kind='bar', ax=ax2, color=palette['secondary'])
    ax2.set_title('Shows by number of Seasons')
    ax2.set_xlabel('Number of Seasons')

    for container in ax2.containers:
        ax2.bar_label(container)

    plt.savefig('images/svg/duration_distribution.svg', format="svg")
    plt.savefig('images/png/duration_distribution.png', format="png", dpi=150, bbox_inches="tight")
duration_distribution()



# ----------------------------
#          REVIEWS
# ----------------------------

pattern = regex.compile(r'[\p{L}]+')

movie_mean_scores = reviews.groupby(['movie'])['rating'].mean()
movie_total_reviews = reviews.groupby(['movie'])['rating'].count()

movie_scores = pd.concat({'mean': movie_mean_scores, 'n_reviews': movie_total_reviews}, axis=1)

def score_distribution():
    fig, ax = plt.subplots()
    sns.histplot(movie_scores['mean'], kde=True, color=palette['secondary'], ax=ax)

    ax.set_title('Titles\' score')
    ax.set_xlabel('Score')
    ax.set_xticks(range(1, 11))

    plt.savefig('images/svg/score_distribution.svg', format="svg")
    plt.savefig('images/png/score_distribution.png', format="png", dpi=150, bbox_inches="tight")
score_distribution()


def rating_distribution():
    fig, ax = plt.subplots()
    reviews.groupby('rating')['movie'].count().plot(kind='bar', color=palette['secondary'], ax=ax)

    ax.set_title('Ratings by users')
    ax.set_xlabel('Rating')
    ax.set_ylabel('Count')

    for container in ax.containers:
        ax.bar_label(container)

    plt.savefig('images/svg/rating_distribution.svg', format="svg")
    plt.savefig('images/png/rating_distribution.png', format="png", dpi=150, bbox_inches="tight")
rating_distribution()


def spoiler_percentage():
    spoiler = reviews['spoiler_tag'].sum() / reviews['spoiler_tag'].count()
    non_spoiler = 1 - spoiler

    fig, ax = plt.subplots()
    ax.barh(0, non_spoiler, alpha=0.9)
    ax.barh(0, spoiler, left=non_spoiler, alpha=0.9)

    # Title & Subtitle
    ax.text(0, 0.5,'Spoiler Reviews', fontsize=22, fontweight='bold')
    ax.text(0, 0.45,'A majority of reviews do not contain spoilers', fontsize=12)

    ax.text(non_spoiler / 2, 0, f'{non_spoiler * 100:.0f}%', color=palette['tertiary'], va='center', ha='center', fontsize=22)
    ax.text(non_spoiler / 2, -0.1, 'Non-Spoiler', color=palette['tertiary'], va='center', ha='center', fontsize=18)
    ax.text(non_spoiler + spoiler / 2, 0, f'{spoiler * 100:.0f}%', color=palette['tertiary'], va='center', ha='center', fontsize=22)
    ax.text(non_spoiler + spoiler / 2, -0.1, 'Spoiler', color=palette['tertiary'], va='center', ha='center', fontsize=18)

    ax.axis('off')

    plt.savefig('images/svg/spoiler_percentage.svg', format="svg")
    plt.savefig('images/png/spoiler_percentage.png', format="png", dpi=150, bbox_inches="tight")
spoiler_percentage()


def word_count_distribution():
    reviews['review_detail_word_count'] = reviews.loc[:, 'review_detail'].apply(lambda s: len(pattern.findall(s)))

    fig, ax = plt.subplots()
    sns.histplot(reviews['review_detail_word_count'], kde=True, color=palette['secondary'], ax=ax, bins='doane')

    ax.set_title('Word count distribution on reviews')
    ax.set_xlim(0, 1200)
    ax.set_xlabel('Number of words in the review')
    ax.set_xlabel('Number of words in the review')
    ax.set_ylabel('Count')

    plt.savefig('images/svg/word_count_distribution.svg', format="svg")
    plt.savefig('images/png/word_count_distribution.png', format="png", dpi=150, bbox_inches="tight")
word_count_distribution()


def word_count_boxplot():
    ax = sns.boxplot(x='rating', y='review_detail_word_count', data=reviews)
    ax.set_title('Word count per review rating')
    ax.set_xlabel('Rating')
    ax.set_ylabel('Word count')
    # ax.set_ylim(None, 750)

    plt.savefig('images/svg/word_count_boxplot.svg', format="svg")
    plt.savefig('images/png/word_count_boxplot.png', format="png", dpi=150, bbox_inches="tight")
word_count_boxplot()


def reviews_distribution():
    fig, ax = plt.subplots()

    reviews_per_reviewer = reviews.groupby('reviewer').count()['movie']
    reviews_per_reviewer[reviews_per_reviewer == reviews_per_reviewer.max()]

    sns.histplot(reviews_per_reviewer, bins="doane", ax=ax, color=palette['secondary'])
    ax.set_title('Reviews per reviewer (reviewers with at least 100 reviews)')
    ax.set_xlabel('Number of reviews')
    ax.set_ylim(0, 700)

    for container in ax.containers:
        ax.bar_label(container)

    plt.savefig('images/svg/reviews_distribution.svg', format="svg")
    plt.savefig('images/png/reviews_distribution.png', format="png", dpi=150, bbox_inches="tight")
reviews_distribution()
