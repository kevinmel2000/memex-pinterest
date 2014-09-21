from flask import request
from mongoutils.memex_mongo_utils import MemexMongoUtils

def request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']

def get_domains():

    mmu = MemexMongoUtils()
    mmu.list_domains()
