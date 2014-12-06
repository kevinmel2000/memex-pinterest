from flask import request
from mongoutils.memex_mongo_utils import MemexMongoUtils
from scrapyutils.scrapydutil import ScrapydJob
from settings import SCREENSHOT_DIR
from mongoutils.known_hosts import KnownHostsCompare

    
def get_screenshot_relative_path(real_path):
    try:
        return real_path.split("static/")[1]
    except IndexError:
        return None

def request_wants_json():

    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']

def hosts_handler(page = 1, which_collection = "crawl-data", filter_field = None, filter_regex = None):
    """Put together host documents for use with hosts endpoint """

    mmu = MemexMongoUtils(which_collection = which_collection)
    khc = KnownHostsCompare()

    host_dics = mmu.list_hosts(page = page, filter_field = filter_field, filter_regex = filter_regex)

    for host_dic in host_dics:

        #host scoring is added here as is known hostedness
        host_dic.pop("_id")
        is_known_host = khc.is_known_host(host_dic["host"])
        host_dic["is_known_host"] = is_known_host
        hsu = mmu.get_highest_scoring_url_with_screenshot(host_dic["host"])
        host_score = mmu.get_host_score(host_dic["host"])
        host_dic["host_score"] = host_score
        
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
        date = url_dic["crawled_at"]
        try:
            url_dic["crawled_at"] = date.isoformat()
        except:
            url_dic["crawled_at"] = str(date)

    return url_dics

def schedule_spider_handler(seed, spider_host = "localhost", spider_port = "6800"):

    mmu = MemexMongoUtils()
    scrapyd_util = ScrapydJob(spider_host, spider_port, screenshot_dir = SCREENSHOT_DIR)
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

def set_score_handler(url, score):
    mmu = MemexMongoUtils()
    mmu.set_score(url, score)   
    


## workspace    
def list_workspace():
    mmu = MemexMongoUtils()
    return mmu.list_workspace()
    
def add_workspace(name):
    mmu = MemexMongoUtils()
    mmu.add_workspace(name)

def set_workspace_selected(id):
    mmu = MemexMongoUtils()
    mmu.set_workspace_selected(id)

def delete_workspace(id):
    mmu = MemexMongoUtils()
    mmu.delete_workspace(id)


##keyword
def list_keyword():
    mmu = MemexMongoUtils()
    return mmu.list_keyword()
    
def save_keyword(list):
    mmu = MemexMongoUtils()
    mmu.save_keyword(list)

def schedule_spider_searchengine_handler(keywords, spider_host = "localhost", spider_port = "6800"):

    mmu = MemexMongoUtils()
    #scrapyd_util = ScrapydJob(spider_host, spider_port, screenshot_dir = SCREENSHOT_DIR)
    #scrapyd_util = ScrapydJob(spider_host, spider_port, project="search-engine", screenshot_dir = SCREENSHOT_DIR)
    scrapyd_util = ScrapydJob(spider_host, spider_port, project="default", screenshot_dir = SCREENSHOT_DIR)
    job_id = scrapyd_util.schedule_keywords(keywords)
    mmu.add_job(keywords, job_id)

    return True



if __name__ == "__main__":
    print "HERE"
    print hosts_handler()