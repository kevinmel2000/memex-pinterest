from flask import request
from mongoutils.memex_mongo_utils import MemexMongoUtils
import json
import itertools

def request_wants_json():

    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']

def hosts_handler(page = 1):
    """Put together host documents for use with hosts endpoint """

    mmu = MemexMongoUtils()

    #!process host records
    #!THIS WON'T SCALE
    mmu.process_host_data()
    host_dics = mmu.list_hosts(page = page)
    for host_dic in host_dics:
        host_dic.pop("_id")

    return host_dics

def urls_handler(host = None):
    """Put together host documents for use with hosts endpoint """

    mmu = MemexMongoUtils()
    url_dics = mmu.list_urls(host = host)

    for url_dic in url_dics:
        url_dic.pop("_id")

    return url_dics

if __name__ == "__main__":
#    for x in hosts_handler():
#        print x["host"]

    for x in hosts_handler(page = 3):
        print x["host"]
#    for x in urls_handler():
#        print x["url"]
