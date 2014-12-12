#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tqdm import tqdm
from ranker import Ranker
from ui.mongoutils.memex_mongo_utils import MemexMongoUtils

def rescore_all():
    """ Rescore all items from mongo """

    mmu = MemexMongoUtils()
    docs = mmu.list_all_urls_iterator(return_html = True)

    ranker = Ranker.load()
    for doc in docs:
        try:
            score = ranker.score_doc(doc)
        except:
            score = 0

        mmu.set_score(doc["url"], score)
        
if __name__ == '__main__':
    rescore_all()
