import sqlite3
import pandas as pd

# TODO!!!! DATE_ADDED / DURATION / FIX TYPE ENUM /EXECUTE MANY/ ATORES REPETIDOS NUM SO FILME

con = sqlite3.connect('test.db')
cur = con.cursor()
cur.execute("BEGIN")


titles = pd.read_csv('data/netflix_titles_clean.csv')
reviews = pd.read_csv('data/reviews_clean.csv')


def get_countries(elem):
    if isinstance(elem, str):
        return list(map(lambda y: y.strip(" "), elem.split(',')))
    else:
        return []


def get_genres(elem):
    return list(map(lambda y: y.strip(" "), elem.split(',')))


def get_persons(elem):
    if isinstance(elem, str):
        return list(map(lambda y: y.strip(" "), elem.split(',')))
    else:
        return []


countries = set()
for elem in titles['country']:
    for c in get_countries(elem):
        countries.add(c)
countries.remove("")
countries = list(countries)
countries_dict = dict()
for idx, c in enumerate(countries):
    countries_dict[c] = idx  # + 1
    cur.execute("insert into country(id, name) values (?, ?)", (idx, c))

genres = set()
for elem in titles['listed_in']:
    for g in get_countries(elem):
        genres.add(g)
genres = list(genres)
genres_dict = dict()
for idx, g in enumerate(genres):
    genres_dict[g] = idx  # + 1
    cur.execute("insert into genre(id, name) values (?, ?)", (idx, g))

persons = set()
for elem in titles['cast']:
    for p in get_persons(elem):
        persons.add(p)
for elem in titles['director']:
    for p in get_persons(elem):
        persons.add(p)
persons = list(persons)
persons_dict = dict()
for idx, p in enumerate(persons):
    persons_dict[p] = idx  # + 1
    cur.execute("insert into person(id, name) values (?, ?)", (idx, p))


for idx, row in titles.iterrows():
    cur.execute("""insert into show(id, title, description, date_added, release_year, duration, rating, type) 
                                    values (?, ?, ?, ?, ?, ?, ?, ?)""",
                (idx, row["title"], row["description"], row["date_added"], row["release_year"], 10, row["rating"], row["type"]))

    for c in get_countries(row["country"]):
        if len(c) > 0:
            cur.execute(
                "insert into country_show(country_id, show_id) values (?, ?)", (countries_dict[c], idx))

    for g in get_genres(row["listed_in"]):
        cur.execute(
            "insert into genre_show(genre_id, show_id) values (?, ?)", (genres_dict[g], idx))
    for p in get_persons(row["cast"]):
        if len(p) > 0:
            cur.execute(
                "select * from actor_show where actor_id = ? and show_id = ?", (persons_dict[p], idx))
            if cur.fetchone() is None:
                con.execute(
                    "insert into actor_show(actor_id, show_id) values (?, ?)", (persons_dict[p], idx))

    for p in get_persons(row["director"]):
        if len(p) > 0:
            cur.execute(
                "select * from director_show where director_id = ? and show_id = ?", (persons_dict[p], idx))
            if cur.fetchone() is None:
                cur.execute(
                    "insert into director_show(director_id, show_id) values (?, ?)", (persons_dict[p], idx))

for idx, row in reviews.iterrows():

    if idx == 0:
        cur.execute("insert into reviewer(id, name) values (?, ?)",
                    (idx, row["reviewer"]))

        cur.execute("""insert into review(id, show_id, rating, title, body, helpful_votes, total_votes, review_date, spoiler, reviewer_id) 
                                        values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (idx, 0, 0, row["review_summary"], row["review_detail"], 1, 2, row["review_date"], row["spoiler_tag"], idx))
    else:
        cur.execute("select id from reviewer where name = ?",
                    (row["reviewer"],))
        res = cur.fetchone()
        if res is not None:
            cur.execute("""insert into review(id, show_id, rating, title, body, helpful_votes, total_votes, review_date, spoiler, reviewer_id) 
                                        values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (idx, 0, 0, row["review_summary"], row["review_detail"], 1, 2, row["review_date"], row["spoiler_tag"], res[0]))
        else:
            cur.execute("SELECT max(id) FROM reviewer")
            res = cur.fetchone()

            cur.execute("insert into reviewer(id, name) values (?, ?)",
                        (res[0] + 1, row["reviewer"]))

            cur.execute("""insert into review(id, show_id, rating, title, body, helpful_votes, total_votes, review_date, spoiler, reviewer_id) 
                                        values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (idx, 0, 0, row["review_summary"], row["review_detail"], 1, 2, row["review_date"], row["spoiler_tag"], res[0] + 1))


cur.execute("COMMIT")
con.close()
