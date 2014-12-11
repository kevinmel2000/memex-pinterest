import itertools
import csv
from pymongo import MongoClient
import traceback
from random import randrange
from operator import itemgetter
from urlparse import urlparse
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from errors import DeletingSelectedWorkspaceError

class MemexMongoUtils(object):

    def __init__(self, init_db=False, address="localhost", port=27017, which_collection="crawl-data"):
        """This class  initializes a Memex Mongo object and rebuilds the db collections if you want.

        Warning: init_db will delete your collection when set to True

        which_collection specifies whether to connect to the scrapy crawl data or common crawl data collection
        to connect to common crawl specify this as cc-crawldata
        """

        self.client = MongoClient(address, port)
        db = self.client["MemexHack"]

        workspace_collection_name = "workspace"
        self.workspace_collection = db[workspace_collection_name]

        seed_collection_name = "seedinfo"

        if which_collection == "cc-crawl-data":
            url_collection_name = "cc-urlinfo"
            host_collection_name = "cc-hostinfo"
        elif which_collection == "known-data":
            url_collection_name = "known-urlsinfo"
            host_collection_name = "known-hostsinfo"
        elif which_collection == "crawl-data":
            # Search for the current selected workspace
            # if empty leave the default
            ws_doc = self.workspace_collection.find_one({"selected" : True})
            if None == ws_doc:
                url_collection_name = "urlinfo"
                host_collection_name = "hostinfo"
            else:
                url_collection_name = "urlinfo" + "-" + ws_doc['name']
                host_collection_name = "hostinfo" + "-" + ws_doc['name']
                seed_collection_name = "seedinfo" + "-" + ws_doc['name']

        else:
            raise Exception("You have specified an invalid collection, please choose either crawl-data or cc-crawl-data for which_collection")

        self.urlinfo_collection = db[url_collection_name]
        self.hostinfo_collection = db[host_collection_name]
        self.seed_collection = db[seed_collection_name]

        if init_db:
            print "Got call to initialize db with %s %s" % (url_collection_name, host_collection_name)
            try:
                print "Dropping %s and %s" % (url_collection_name, host_collection_name)
                db.drop_collection(url_collection_name)
                db.drop_collection(host_collection_name)
                db.drop_collection(seed_collection_name)

            except:
                print "handled:"
                traceback.print_exc()

            db.create_collection(url_collection_name)
            db.create_collection(host_collection_name)
            db.create_collection(seed_collection_name)

            # create index and drop any dupes
            self.urlinfo_collection.ensure_index("url", unique=True, drop_dups=True)
            self.hostinfo_collection.ensure_index("host", unique=True, drop_dups=True)
            self.seed_collection.ensure_index("url", unique=True, drop_dups=True)

    def init_workspace(self, address="localhost", port=27017):
        db = self.client["MemexHack"]
        workspace_collection_name = "workspace"
        self.workspace_collection = db[workspace_collection_name]
        res = self.workspace_collection.find();
        docs = list(res)
        for doc in docs:
            self.delete_workspace_related(doc['name'])
        
        print "Dropping %s" % (workspace_collection_name)
        db.drop_collection(workspace_collection_name)
        db.create_collection(workspace_collection_name)
        self.add_workspace("default")
        self.set_workspace_selected_by_name("default")
        
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

    def add_job(self, url, job_id, project, spider, default_state="Initializing"):

        try:
            seed_doc = {"url" : url, "state" : default_state, "job_id" : job_id, "project" : project, "spider" : spider}
            self.seed_collection.save(seed_doc)
        except Exception:
            self.seed_collection.update({"url" : url}, {'$set' : {"job_id" : job_id}})

    def list_seed_docs(self):
        return list(self.seed_collection.find())        

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

#####################   workspace  #####################
    def list_workspace(self):
        docs = self.workspace_collection.find()
        return list(docs)

    def add_workspace(self, name):
        self.workspace_collection.save({'name':name, 'selected': False})


        url_collection_name = "urlinfo" + "-" + name
        host_collection_name = "hostinfo" + "-" + name
        seed_collection_name = "seedinfo" + "-" + name

        db = self.client["MemexHack"]
        db.create_collection(url_collection_name)
        db.create_collection(host_collection_name)
        db.create_collection(seed_collection_name)

        # create index and drop any dupes
        db[url_collection_name].ensure_index("url", unique=True, drop_dups=True)
        db[host_collection_name].ensure_index("host", unique=True, drop_dups=True)
        db[seed_collection_name].ensure_index("url", unique=True, drop_dups=True)


    def get_workspace_by_id(self,id):
        return self.workspace_collection.find_one({"_id" : ObjectId( id )})
        

    def set_workspace_selected_by_name(self, name):
        self.workspace_collection.update({}, {'$set' : {"selected" : False}}, multi=True)
        self.workspace_collection.update({"name" : name}, {'$set' : {"selected" : True}})

    def set_workspace_selected(self, id):
        self.workspace_collection.update({}, {'$set' : {"selected" : False}}, multi=True)
        self.workspace_collection.update({"_id" : ObjectId( id )}, {'$set' : {"selected" : True}})

    def get_workspace_selected(self):
        return self.workspace_collection.find_one({"selected" : True})

    def delete_workspace(self, id):
        ws_doc = self.workspace_collection.find_one({"_id" : ObjectId( id )})
        if ws_doc["selected"] == True:
            raise DeletingSelectedWorkspaceError('Deleting the selected workspace is not allowed')
        else:   
            self.delete_workspace_related(ws_doc['name'])
            self.workspace_collection.remove({"_id" : ObjectId( id )})

    def delete_workspace_related(self,name):
        db = self.client["MemexHack"]
        print "Dropping %s" % ("urlinfo" + "-" + name)
        db["urlinfo" + "-" + name].drop()
        print "Dropping %s" % ("hostinfo" + "-" + name)
        db["hostinfo" + "-" + name].drop()
        print "Dropping %s" % ("seedinfo" + "-" + name)
        db["seedinfo" + "-" + name].drop()
        
        

#####################   keyword  #####################
    def list_keyword(self):
        ws = self.get_workspace_selected()

        if ws == None or "keyword" not in ws or ws["keyword"] == None:
            return []
        else:
            return list(ws["keyword"])

    def save_keyword(self, keywords):
        ws = self.get_workspace_selected()
        if ws == None:
            self.workspace_collection.upsert({"_id" : "_default"}, {'$set' : {"keyword" : keywords}})
        else:
            self.workspace_collection.update({"_id" : ObjectId(ws["_id"] )}, {'$set' : {"keyword" : keywords}})

####################   search term  #####################
    def list_search_term(self):
        ws = self.get_workspace_selected()

        if ws == None or "searchterm" not in ws or ws["searchterm"] == None:
            return []
        else:
            return list(ws["searchterm"])

    def save_search_term(self, search_terms):

        ws = self.get_workspace_selected()
        if ws == None:
            self.workspace_collection.upsert({"_id" : "_default"}, {'$set' : {"searchterm" : search_terms}})
        else:
            self.workspace_collection.update({"_id" : ObjectId(ws["_id"] )}, {'$set' : {"searchterm" : search_terms}})

if __name__ == "__main__":

    mmu = MemexMongoUtils(which_collection="known-data")
    print mmu.list_all_urls()
    print mmu.list_all_hosts()

    #mmu.save_search_term(['blahg'])
#    print mmu.list_search_term()
#    print mmu.seed_collection
#    print mmu.list_seed_docs()
    
    #MemexMongoUtils(which_collection="crawl-data", init_db=True)
    #MemexMongoUtils(which_collection="known-data", init_db=True)
    #MemexMongoUtils(which_collection="cc-crawl-data", init_db=True)
    #mmu.init_workspace()