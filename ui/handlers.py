from flask import request
from mongoutils.memex_mongo_utils import MemexMongoUtils
from scrapyutils.scrapydutil import ScrapydJob
import json
import itertools

def get_screenshot_relative_path(real_path):

    return real_path.split("static/")[1]

def request_wants_json():

    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']

def hosts_handler(page = 1, which_collection = "crawl-data"):
    """Put together host documents for use with hosts endpoint """

    mmu = MemexMongoUtils(which_collection = which_collection)

    #!process host records
    #!THIS WON'T SCALE
    mmu.process_host_data()
    host_dics = mmu.list_hosts(page = page)

    for host_dic in host_dics:
        host_dic.pop("_id")
        hsu = mmu.get_highest_scoring_url_with_screenshot(host_dic["host"])
        if hsu:
            screenshot_path = get_screenshot_relative_path(hsu['screenshot_path'])
            host_dic["hsu_screenshot_path"] = screenshot_path
        else:
            host_dic["hsu_screenshot_path"] = None

    return host_dics

def urls_handler(host = None, which_collection  = "crawl-data"):
    """Put together host documents for use with hosts endpoint """

    mmu = MemexMongoUtils(which_collection = which_collection)
    url_dics = mmu.list_urls(host = host)

    for url_dic in url_dics:
        url_dic.pop("_id")

    return url_dics

def schedule_spider_handler(seed, spider_host = "localhost", spider_port = "6800"):

    mmu = MemexMongoUtils()
    scrapyd_util = ScrapydJob(spider_host, spider_port)
    job_id = scrapyd_util.schedule(seed)
    mmu.add_job(seed, job_id)

    return True

def get_job_state_handler(url, spider_host = "localhost", spider_port = "6800"):
    
    mmu = MemexMongoUtils()
    scrapyd_util = ScrapydJob(spider_host, spider_port)
    job_id = mmu.get_seed_doc(url)["job_id"]

    return scrapyd_util.get_state(job_id)    

def discovery_handler():

    mmu = MemexMongoUtils()
    seeds = mmu.list_seeds()
    return seeds

def mark_interest_handler(interest, url):

    mmu = MemexMongoUtils()
    if interest:
        mmu.set_interest(url, True)

    else:
        #if user marks url as uninteresting, score drops to 0
        mmu.set_interest(url, False)

        #!should we be doing this?
#        mmu.set_score(url, 0)

if __name__ == "__main__":

    print schedule_spider_handler("http://butts.com/")
#    for x in hosts_handler(page = 3):
#        print x["host"]

#    print "===================================+"
#    for x in hosts_handler(page = 3, which_collection = "cc-crawl-data"):
#        print x["host"]
