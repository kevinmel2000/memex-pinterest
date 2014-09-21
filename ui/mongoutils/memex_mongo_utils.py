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

            except:
                print "handled:"
                traceback.print_exc()

            db.create_collection("urlinfo")

        self.urlinfo_collection = db.urlinfo

        #create index and drop any dupes
        if init_db:
            self.urlinfo_collection.ensure_index("url", unique = True, drop_dups = True)

    def list_urls(self):

        docs = self.urlinfo_collection.find(fields = {"url" : 1, "host" : 1, "score" : 1, "html" : 1})

        return list(docs)

    def insert_test_data(self, test_fn = "test_sites.csv"):

        with open(test_fn) as testfile:
            reader = csv.DictReader(testfile)

            for url_dic in reader:
                try:
                    if not "score" in url_dic:
                        url_dic["score"] = randrange(100)

                    self.urlinfo_collection.save(url_dic)

                except:
                    #doc with same url exists, skip                                                                                                                                                               
                    pass

if __name__ == "__main__":

    mmu = MemexMongoUtils(init_db = True)
    mmu.insert_test_data()
    for host_doc in mmu.list_hosts():
        print host_doc
