from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import json
import time

INDEX_NAME = "index"


def generate_actions():

    # https://elasticsearch-py.readthedocs.io/en/v7.16.0/helpers.html
    with open("data/json/netflix.json", mode="r") as f:
        data = json.load(f)

        for doc in data:
            action = {
                "_id": doc["show_id"],
                '_op_type': 'index',
                '_index': INDEX_NAME,
                '_source': doc
            }

            yield action


if __name__ == "__main__":
    # instantiate the elastic search client
    es = Elasticsearch(
        hosts=[{'host': "localhost", 'port': 9200}],
        timeout=300
    )

    # Create index and mapping
    mapping = json.load(open("mapping.json", "r"))

    if not es.indices.exists(index=INDEX_NAME):
        print("Index '" + INDEX_NAME + "' doesn't exist. Creating...")
        es.indices.create(index=INDEX_NAME, body=mapping)
    else:
        es.indices.delete(index=INDEX_NAME)
        es.indices.create(index=INDEX_NAME, body=mapping)
        print("Index '" + INDEX_NAME + "' already exists. Recreating...")

    # data = json.load(open("data/json/netflix_test.json", "r"))
    # start = time.time()
    # for i in range(len(data)):
    #     res = es.index(index='index', doc_type="_doc",
    #                    id=data[i]['show_id'], document=data[i])

    # end = time.time()
    # print("Took", round(end - start, 3), "seconds to upload all documents")

    start = time.time()

    bulk(es, actions=generate_actions())

    end = time.time()
    print("Took", round(end - start, 3), "seconds to upload all documents")
