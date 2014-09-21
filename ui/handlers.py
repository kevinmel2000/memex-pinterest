from flask import request
from mongoutils.memex_mongo_utils import MemexMongoUtils
import itertools

def request_wants_json():

    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']


def hosts_handler():
    """Put together host documents for use with hosts endpoint """

    mmu = MemexMongoUtils()
    hosts = mmu.list_urls()
    for host in hosts:
        host.pop("_id")

    host_dics = []
    for key, group in itertools.groupby(hosts, lambda item: item["host"]):
        host_dic = {}
        group_list = list(group)
        host_dic["host"] = key
        host_dic["num_urls"] = len(group_list)

        #calculate score, normalized
        host_score = 0
        for url_dic in group_list:
            host_score += int(url_dic["score"])

        host_score = int(host_score / host_dic["num_urls"])
        host_dic["host_score"] = host_score

        host_dics.append(host_dic)

    return host_dics

if __name__ == "__main__":
    print hosts_handler()
