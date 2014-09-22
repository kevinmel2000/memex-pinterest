import itertools
import csv
from pymongo import MongoClient
import traceback
from random import randrange

class MemexMongoUtils(object):

    def __init__(self, init_db = False, address = "localhost", port = 27017):

        self.client = MongoClient(address, port)

        db = self.client["MemexHack"]

        if init_db:
            print "Got call to initialize db"
            try:
                db.drop_collection("urlinfo")
                db.drop_collection("hostinfo")

            except:
                print "handled:"
                traceback.print_exc()

            db.create_collection("urlinfo")
            db.create_collection("hostinfo")

        self.urlinfo_collection = db.urlinfo
        self.hostinfo_collection = db.hostinfo

        #create index and drop any dupes
        if init_db:
            self.urlinfo_collection.ensure_index("url", unique = True, drop_dups = True)
            self.hostinfo_collection.ensure_index("host", unique = True, drop_dups = True)

    def list_urls(self, host = None, limit = 20):

        if not host:
            docs = self.urlinfo_collection.find().sort("score", -1).limit(20)
        else:
            docs = self.urlinfo_collection.find({"host" : host}).sort("score", -1).limit(20)

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

    def list_all_urls(self):

        docs = self.urlinfo_collection.find()

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

            #calculate score, sum(individual scores)/number of urls
            host_score = 0
            for url_dic in group_list:
                host_score += int(url_dic["score"])

            host_score = int(host_score / host_dic["num_urls"])
            host_dic["host_score"] = host_score

            host_dics.append(host_dic)

        for host_dic in host_dics:
            try:
                self.hostinfo_collection.save(host_dic)
            except:
                pass

        return host_dics

    def insert_test_data(self):

        self.__insert_url_test_data()
        self.process_host_data()

if __name__ == "__main__":

    mmu = MemexMongoUtils(init_db = True)
    mmu.insert_test_data()
#    hosts = []
#    for x in mmu.process_host_data():
#        print x["host"]

#    for x in mmu.list_hosts(page = 1):
#        print x

#    for x in mmu.list_hosts(page = 2):
#        print x

    for x in mmu.list_all_hosts():
        print x
    