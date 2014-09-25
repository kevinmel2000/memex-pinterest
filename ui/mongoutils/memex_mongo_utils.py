import random
import itertools
import csv
from pymongo import MongoClient
import traceback
from random import randrange
import json
from operator import itemgetter

class MemexMongoUtils(object):

    def __init__(self, init_db = False, address = "localhost", port = 27017, which_collection = "crawl-data"):
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

        print db.collection_names()
        #create index and drop any dupes
        if init_db:
            self.urlinfo_collection.ensure_index("url", unique = True, drop_dups = True)
            self.hostinfo_collection.ensure_index("host", unique = True, drop_dups = True)
            self.seed_collection.ensure_index("url", unique = True, drop_dups = True)


    def list_urls(self, host = None, limit = 20):

        if not host:
            docs = self.urlinfo_collection.find().sort("score", -1).limit(limit)
        else:
            docs = self.urlinfo_collection.find({"host" : host}).sort("score", -1).limit(limit)

        return list(docs)

    def list_hosts(self, page = 1, num_docs = 21):

        try:
            docs = self.hostinfo_collection.find().sort("host_score", -1).skip(num_docs * (page - 1)).limit(num_docs)
        except:
            docs = self.hostinfo_collection.find().sort("host_score", -1).limit(num_docs)
            
        return list(docs)

    def list_all_hosts(self):

        docs = self.hostinfo_collection.find()
            
        return list(docs)

    def list_all_urls(self, sort_by = "host"):

        docs = self.urlinfo_collection.find().sort(sort_by, 1)

        return list(docs)

    def list_seeds(self, sort_by = "url"):

        docs = self.seed_collection.find().sort(sort_by, 1)

        return list(docs)

    def __insert_url_test_data(self, test_fn = "test_sites.csv"):

        with open(test_fn) as testfile:
            reader = csv.DictReader(testfile)

            #insert url data
            for url_dic in reader:
                try:
                    if not "score" in url_dic:
                        url_dic["score"] = randrange(100)

                    self.urlinfo_collection.save(url_dic)

                except:
                    print url_dic
                    traceback.print_exc()
                    #doc with same url exists, skip
                    pass

    def process_host_data(self):
        """Insert data into domain collection, requires docs to be indexed already
        e.g. through __insert_url_test_data"""

        hosts = self.list_all_urls()
        for host in hosts:
            host.pop("_id")

        host_dics = []
        for key, group in itertools.groupby(hosts, lambda item: item["host"]):
            host_dic = {}
            group_list = list(group)
            host_dic["host"] = key
            host_dic["num_urls"] = len(group_list)

            #calculate score
            host_score = 0
            for url_dic in group_list:
                if "score" in url_dic:
                    if int(url_dic["score"]) > host_score:
                        host_score = int(url_dic["score"])

            host_dic["host_score"] = host_score

            host_dics.append(host_dic)

        for host_dic in host_dics:
            try:
                self.hostinfo_collection.save(host_dic)
            except:
                pass

        return host_dics

    def insert_test_data(self, test_fn = "test_sites.csv"):

        self.__insert_url_test_data(test_fn = test_fn)
        self.process_host_data()

    def add_job(self, url, job_id, default_state = "Initializing"):

        try:
            seed_doc = {"url" : url, "state" : default_state, "job_id" : job_id}
            self.seed_collection.save(seed_doc)
        except:
            self.seed_collection.update({"url" : url}, {'$set' : {"job_id" : job_id}})

    def mark_seed_state(self, url, state):
        
        self.seed_collection.update({"url" : url}, {'$set': {'state': state}})

    def get_highest_scoring_url_with_screenshot(self, host):

        docs = list(self.urlinfo_collection.find({'$and' : [{'screenshot_path' : {"$exists" : "true"}}, {'host' : host}]}))
        for doc in docs:
            if not "score" in doc:
                doc["score"] = 0

        urls_sorted = sorted(docs, key=itemgetter('score'), reverse = True)

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

if __name__ == "__main__":

    mmu = MemexMongoUtils(which_collection = "crawl-data")
#    for doc in mmu.list_all_urls():
#        mmu.set_score(doc["url"], random.randint(0,100))

    print mmu.get_highest_scoring_url_with_screenshot('freebsd.orgddd')

#    mmu.add_seed("http://www.hyperiongray.com")
#    mmu.mark_seed_state("http://www.hyperiongray.com", "Running")
#    print mmu.get_seed_doc("http://www.hyperiongray.com")

#    for x in mmu.list_seeds():
#        print x['url'], x['job_id']
#    mmu.insert_test_data(test_fn = "test_sites.csv")

#    mmu = MemexMongoUtils(init_db = True, which_collection = "crawl-data")
#    mmu.insert_test_data("test_sites.csv")

#    hosts = []
#    for x in mmu.process_host_data():
#        print x["host"]
#
#    for x in mmu.list_urls(host = "bhphotovideo.com"):
#        print x
#
#    for x in mmu.list_all_urls():
#        print x
#
#    for x in mmu.list_all_hosts():
#        print x
#    print len(mmu.list_all_hosts())
