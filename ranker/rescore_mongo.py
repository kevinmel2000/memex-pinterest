#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymongo
from tqdm import tqdm
from ranker import Ranker


def _get_collection():
    return pymongo.MongoClient()["MemexHack"].urlinfo


def get_mdocs(collection):
    return collection.find(
        {},
        #{"interest": {"$exists": False}},
        {"html": 1, "html_rendered": 1}
    )


def rescore_all():
    """ Rescore all items from mongo """
    ranker = Ranker.load()
    coll = _get_collection()
    for doc in tqdm(get_mdocs(coll), leave=True):
        score = ranker.score_doc(doc)
        coll.update({'_id': doc['_id']}, {"$set": {"score": score}})
    print("")


if __name__ == '__main__':
    rescore_all()
