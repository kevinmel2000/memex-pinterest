import traceback
from urlparse import urlparse
from memex_mongo_utils import MemexMongoUtils
import csv

def import_known_ads(csv_filename, limit = 2000):

    mmu = MemexMongoUtils(which_collection = "known-data", init_db = True)
    with open(csv_filename) as testfile:
        reader = csv.DictReader(testfile)

        c = 0
        for url_dic in reader:
            try:
                host = urlparse(url_dic["url"]).netloc
                if ":" in host:
                    host = host.split(":")[0]
                if not host or "." not in host:
                    raise Exception("Bad host, skipping")
                url_dic["host"] = host
                url_dic["crawled_at"] = url_dic["importtime"]
                url_dic.pop("importtime")
            
            except:
                print "Skipping record %s because: " % str(url_dic)
                traceback.print_exc()
                continue
                
            mmu.urlinfo_collection.update({"url" : url_dic["url"]}, url_dic, upsert = True)
            c += 1
            if c == limit:
                print "Import limit reached"
                break
    
    mmu.process_host_data()
    
    
if __name__ == "__main__":

    mmu = MemexMongoUtils(which_collection = "known-data", init_db = True)    
    import_known_ads("/home/memex-punk/Desktop/known_sites.csv")
    mmu.process_host_data()
    for host in mmu.list_all_hosts():
        print host
