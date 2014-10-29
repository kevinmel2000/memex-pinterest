import itertools
import csv
from pymongo import MongoClient
import traceback
from random import randrange
from operator import itemgetter
from urlparse import urlparse
from pymongo.errors import DuplicateKeyError

class MemexMongoUtils(object):

    def __init__(self, init_db=False, address="localhost", port=27017, which_collection="crawl-data"):
        """This class  initializes a Memex Mongo object and rebuilds the db collections if you want.

        Warning: init_db will delete your collection when set to True

        which_collection specifies whether to connect to the scrapy crawl data or common crawl data collection
        to connect to common crawl specify this as cc-crawldata
        """

        if which_collection == "crawl-data":
            url_collection_name = "urlinfo"
            host_collection_name = "hostinfo"

        elif which_collection == "cc-crawl-data":
            url_collection_name = "cc-urlinfo"
            host_collection_name = "cc-hostinfo"

        elif which_collection == "known-data":
            url_collection_name = "known-urlsinfo"
            host_collection_name = "known-hostsinfo"

        else:
            raise Exception("You have specified an invalid collection, please choose either crawl-data or cc-crawl-data for which_collection")

        self.client = MongoClient(address, port)

        db = self.client["MemexHack"]

        if init_db:
            print "Got call to initialize db with %s %s" % (url_collection_name, host_collection_name)
            try:
                print "Dropping %s and %s" % (url_collection_name, host_collection_name)
                db.drop_collection(url_collection_name)
                db.drop_collection(host_collection_name)
                db.drop_collection("seeds")

            except:
                print "handled:"
                traceback.print_exc()

            db.create_collection(url_collection_name)
            db.create_collection(host_collection_name)
            db.create_collection("seeds")

        self.urlinfo_collection = db[url_collection_name]
        self.hostinfo_collection = db[host_collection_name]
        self.seed_collection = db["seeds"]

        # create index and drop any dupes
        if init_db:
            self.urlinfo_collection.ensure_index("url", unique=True, drop_dups=True)
            self.hostinfo_collection.ensure_index("host", unique=True, drop_dups=True)
            self.seed_collection.ensure_index("url", unique=True, drop_dups=True)

    def list_indexes(self):
        
        return self.hostinfo_collection.index_information()

    def list_urls(self, host=None, limit=20):

        if not host:
            docs = self.urlinfo_collection.find().sort("score", -1).limit(limit)
        else:
            docs = self.urlinfo_collection.find({"host" : host}).sort("score", -1).limit(limit)

        return list(docs)

    def list_hosts(self, page=1, num_docs=28, filter_regex = None, filter_field = None):

        if filter_regex and filter_field:
            docs = self.hostinfo_collection.find({filter_field:{'$regex':filter_regex}})
        else:
            docs = self.hostinfo_collection.find().sort("host_score", -1)
        
        try:
            docs = docs.skip(num_docs * (page - 1)).limit(num_docs)
        except Exception:
            docs = docs.limit(num_docs)

        docs_list = list(docs.limit(num_docs))
            
        return docs_list

    def list_all_hosts(self):

        docs = self.hostinfo_collection.find()

        return list(docs)

    def list_all_urls(self, sort_by="host"):

        docs = self.urlinfo_collection.find({}, {'html':0, 'html_rendered': 0})  # .sort(sort_by, 1)

        return sorted(list(docs), key=lambda rec: rec[sort_by])

    def list_seeds(self, sort_by="url"):

        docs = self.seed_collection.find().sort(sort_by, 1)

        return list(docs)

    def __insert_url_test_data(self, test_fn="test_sites.csv"):

        with open(test_fn) as testfile:
            reader = csv.DictReader(testfile)

            # insert url data
            for url_dic in reader:
                try:
                    if not "score" in url_dic:
                        url_dic["score"] = randrange(100)

                    self.urlinfo_collection.save(url_dic)

                except:
                    print url_dic
                    traceback.print_exc()
                    # doc with same url exists, skip
                    pass

    def insert_url(self, **kwargs):
        '''
        Inserts a URL and properly increments the needed host document
        
        is_seed,crawled_at,title,url,link_url,link_text,html_rendered,referrer_depth,depth,total_depth,host,referrer_url,html        
        '''

        url = kwargs["url"]
        host = urlparse(url).netloc
        if ":" in host:
            host = host.split(":")[0]
            
        url_doc = kwargs
        if not "host" in url_doc:
            url_doc["host"] = host
        
        #throws exception if URL already exists, user of method
        #should take this into account
        self.urlinfo_collection.save(kwargs)
        host_doc = {"host" : host, "num_urls" : 1, "host_score" : None}

        #try to insert a new host doc, if fail increment url count
        try:
            self.hostinfo_collection.save(host_doc)
        except DuplicateKeyError:
            self.hostinfo_collection.update({"host" : host}, {"$inc" : {"num_urls" : 1}})

    def get_host_score(self, host):

        high_score_doc = self.urlinfo_collection.find_one({"host" : host}, sort = [("score", -1)])
        if "score" in high_score_doc:
            return high_score_doc["score"]
        else:
            return 0

    def insert_test_data(self, test_fn="test_sites.csv"):

        self.__insert_url_test_data(test_fn=test_fn)

    def add_job(self, url, job_id, default_state="Initializing"):

        try:
            seed_doc = {"url" : url, "state" : default_state, "job_id" : job_id}
            self.seed_collection.save(seed_doc)
        except Exception:
            self.seed_collection.update({"url" : url}, {'$set' : {"job_id" : job_id}})

    def mark_seed_state(self, url, state):

        self.seed_collection.update({"url" : url}, {'$set': {'state': state}})

    def get_highest_scoring_url_with_screenshot(self, host):

        docs = list(self.urlinfo_collection.find({'$and' : [{'screenshot_path' : {"$exists" : "true"}}, {'host' : host}]}))
        for doc in docs:
            if not "score" in doc:
                doc["score"] = 0

        urls_sorted = sorted(docs, key=itemgetter('score'), reverse=True)

        if urls_sorted:
            return urls_sorted[0]
        else:
            return None

    def get_seed_doc(self, url):

        seed_doc = self.seed_collection.find_one({"url" : url})
        return seed_doc

    def set_interest(self, url, interest):

        self.urlinfo_collection.update({"url" : url}, {'$set' : {"interest" : interest}})

    def set_score(self, url, score_set):

        self.urlinfo_collection.update({"url" : url}, {'$set' : {"score" : score_set}})
        
    def set_screenshot_path(self, url, screenshot_path):

        self.urlinfo_collection.update({"url" : url}, {'$set' : {"screenshot_path" : screenshot_path}})        

    def delete_urls_by_match(self, match, negative_match = False):
        """Remove hosts and urls by matching URLs"""

        url_dics = self.list_all_urls()
        for url_dic in url_dics:
            if negative_match:
                if not match in url_dic["url"]:                    
                    self.hostinfo_collection.remove({"host" : url_dic["host"]})
                    self.urlinfo_collection.remove({"url" : url_dic["url"]})
            else:
                if match in url_dic["url"]:
                    self.hostinfo_collection.remove({"host" : url_dic["host"]})
                    self.urlinfo_collection.remove({"url" : url_dic["url"]})

    def delete_hosts_by_match(self, match, negative_match = False):
        """Remove hosts and urls by matching hosts"""

        host_dics = self.list_all_hosts()
        for host_dic in host_dics:
            if negative_match:
                if not match in host_dic["host"]:                    
                    self.hostinfo_collection.remove({"host" : host_dic["host"]})
                    self.urlinfo_collection.remove({"host" : host_dic["host"]})
            else:
                if match in host_dic["host"]:
                    self.hostinfo_collection.remove({"host" : host_dic["host"]})
                    self.urlinfo_collection.remove({"host" : host_dic["host"]})

    def delete_all_by_match(self, match, negative_match = False):
        """Remove hosts and urls by matching both urls and hosts"""

        self.delete_urls_by_match(match, negative_match = negative_match)
        self.delete_hosts_by_match(match, negative_match = negative_match)

if __name__ == "__main__":

    mmu = MemexMongoUtils()
    MemexMongoUtils(which_collection="crawl-data", init_db=True)
    MemexMongoUtils(which_collection="known-data", init_db=True)
    MemexMongoUtils(which_collection="cc-crawl-data", init_db=True)
