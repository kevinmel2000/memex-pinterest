import csv
from pymongo import MongoClient
import traceback

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

    def list_hosts(self):

        docs = self.urlinfo_collection.distinct("host")
        return list(docs)

    def insert_test_data(self, test_fn = "test_sites.csv"):

        with open(test_fn) as testfile:
            reader = csv.DictReader(testfile)
            for url_dic in reader:
                try:
                    self.urlinfo_collection.save(url_dic)
                except:
                    #doc with same url exists, skip                                                                                                                                                               
                    pass

if __name__ == "__main__":

#    mmu = MemexMongoUtils(init_db = True)
#    mmu.insert_test_data()
    mmu = MemexMongoUtils()
    print mmu.list_hosts()
