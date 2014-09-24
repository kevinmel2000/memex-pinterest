from scrapyd_api import ScrapydAPI
import requests
import time
import traceback

class ScrapydJob(object):

    def __init__(self, scrapyd_host = "localhost", scrapyd_port = "6800", project = "discovery", spider = "website_finder"):

        scrapy_url = "http://" + scrapyd_host + ":" + scrapyd_port
        self.scrapi = ScrapydAPI(scrapy_url)
        self.project = project
        self.spider = spider

    def schedule(self, seed):

        self.job_id = self.scrapi.schedule(self.project, self.spider, seed_urls = seed)
        return self.job_id

    def list_jobs(self):
        return self.scrapi.list_jobs(self.project)

    def get_state(self, job_id):

        try:
            for job in self.scrapi.list_jobs(self.project)["running"]:
                print job_id, job["id"]
                if job["id"] == job_id:
                    return "Running"

            for job in self.scrapi.list_jobs(self.project)["pending"]:
                print job_id, job["id"]
                if job["id"] == job_id:
                    return "Pending"

        except:
            print "handled exception:"
            return None

        return "Done"

if __name__ == "__main__":

    scrapy_util = ScrapydJob()
    jid = scrapy_util.schedule("http://www.hyperiongray.com/")
    print scrapy_util.get_state(jid)
#    print scrapy_util.list_jobs()
