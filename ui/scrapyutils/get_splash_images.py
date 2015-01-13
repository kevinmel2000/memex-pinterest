from __future__ import absolute_import

import sys
sys.path.append("../../../")
import requests
import os
import json
import base64
from hashlib import md5
import scrapy
from crawler.discovery.urlutils import (
    add_scheme_if_missing,
    is_external_url,
    get_domain,
)
from ui.mongoutils.memex_mongo_utils import MemexMongoUtils
from crawler.discovery.settings import SPLASH_URL


class SplashGet(object):
    """Manually get a splash screenshot"""

    def __init__(self, screenshot_dir, which_collection = "crawl-data"):
        self.mmu = MemexMongoUtils(which_collection = which_collection)
        self.screenshot_dir = screenshot_dir

    def makedir(self, path):
        try:
            os.makedirs(path)
        except OSError:
            pass
    
    def splash_request(self, url):

        splash_response = requests.get(SPLASH_URL + '/render.json?url=%s&html=1&png=1&wait=2.0&width=640&height=480&timeout=60&images=0' % url)
        return splash_response

    def save_screenshot(self, prefix, data):
        png = base64.b64decode(data['png'])
        dirname = os.path.join(self.screenshot_dir, prefix)
        self.makedir(dirname)
    
        fn = os.path.join(dirname, md5(png).hexdigest() + '.png')
        with open(fn, 'wb') as fp:
            fp.write(png)
        return fn

    def process_splash_response(self, url, splash_response):
        data = json.loads(splash_response.text, encoding='utf8')
    
        screenshot_path = self.save_screenshot(get_domain(url), data)
        html_rendered = data["html"]
        
        return screenshot_path, html_rendered

    def request_and_save(self, url):
        print "Getting screenshot for %s" % url
        splash_response = self.splash_request(url)
        screenshot_path, html_rendered = self.process_splash_response(url, splash_response)
        self.mmu.set_screenshot_path(url, screenshot_path)
        self.mmu.set_html_rendered(url, html_rendered)

    def resolve_images_by_host(self, host):
        url_dics = self.mmu.list_urls(host, limit=2000)
        for url_dic in url_dics:
            self.request_and_save(url_dic["url"])

    def resolve_images_by_url_match(self, match_term):
        url_dics = self.mmu.list_all_urls()
        for url_dic in url_dics:
            #get only if it doesn't have an existing screenshot            
            if "screenshot_path" not in url_dic:
                #!string matching for now, makes more sense as regex
                if match_term in url_dic["url"]:
                    self.request_and_save(url_dic["url"])

    def resolve_images_by_host_match(self, match_term):
        url_dics = self.mmu.list_all_urls()
        for url_dic in url_dics:
            #get only if it doesn't have an existing screenshot
            if "screenshot_path" not in url_dic:
                #!string matching for now, makes more sense as regex
                if match_term in url_dic["host"]:
                    self.request_and_save(url_dic["url"])

if __name__ == "__main__":
    
    sg = SplashGet(screenshot_dir = "/home/ubuntu/memex-pinterest-git/ui/static/images/screenshots")
    #sg.request_and_save("http://duskgytldkxiuqc6.onion/fedpapers/federa23.htm")
    sg.resolve_images_by_host_match(".onion")