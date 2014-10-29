import traceback
from urlparse import urlparse
#from memex_mongo_utils import MemexMongoUtils
import csv
import tldextract

def import_known_ads(csv_filename, limit = 20000000000):

#    mmu = MemexMongoUtils(which_collection = "known-data")
    with open(csv_filename) as testfile:
        reader = csv.DictReader(testfile)

        c = 0
        listed_domains = []
        for url_dic in reader:
            try:
                host = urlparse(url_dic["url"]).netloc
                ext = tldextract.extract(url_dic["url"])
                domain = ext.domain + "." + ext.suffix

                if ":" in host:
                    host = host.split(":")[0]
                if not host or "." not in host:
                    raise Exception("Bad host, skipping")
                if domain not in listed_domains:
                    c += 1
                    print domain
                    listed_domains.append(domain)
                url_dic["host"] = host
                url_dic["crawled_at"] = url_dic["importtime"]
                url_dic.pop("importtime")
            
            except:
#                print "Skipping record %s because: " % str(url_dic)
#                traceback.print_exc()
                continue
                
#            mmu.urlinfo_collection.update({"url" : url_dic["url"]}, url_dic, upsert = True)
            if c == limit:
#                print "Import limit reached"
                break
    print c    
    
if __name__ == "__main__":

    import_known_ads("/home/memex-punk/Desktop/known_sites.csv", limit = 5000)