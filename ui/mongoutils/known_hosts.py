from memex_mongo_utils import MemexMongoUtils

class KnownHostsCompare(object):

    def __init__(self):
        mmu = MemexMongoUtils(which_collection = "known-data")

        #!very inefficient, but such is life
        self.known_hosts_list = [host_dic["host"] for host_dic in mmu.list_all_hosts()]

    def is_known_host(self, host):        
        if host in self.known_hosts_list:
            return True
        else:
            return False

if __name__ == "__main__":
    khc = KnownHostsCompare()
    print khc.is_known_host("201-993-9388.escortsincollege.com")