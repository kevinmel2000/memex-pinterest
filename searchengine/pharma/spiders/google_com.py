# -*- coding: utf-8 -*-
import urllib
from urlparse import urljoin

import scrapy
from w3lib.url import url_query_parameter
try:
    from searchengine.pharma.spiders.basesearchengine import BaseSearchEngineSpider
except:
    from pharma.spiders.basesearchengine import BaseSearchEngineSpider

class GoogleComSpider(BaseSearchEngineSpider):
    name = "google.com"

    download_delay = 2
    search_results_per_page = 20

    def get_search_request(self, phrase, offset=0):
        encoded_phrase = urllib.quote(phrase.encode('utf-8'), '')
        url = ('https://www.google.com/search?q={}&num={}&start={}'
               .format(encoded_phrase,
                       self.search_results_per_page,
                       offset))
        return scrapy.Request(url)

    def get_search_results_requests(self, response):
        sel = scrapy.Selector(response)
        for url in sel.css('h3.r a::attr(href)').extract():
            if 'google.com/url' in url:
                url = url_query_parameter(url, 'url')
                referer = urljoin(response.url, url)
            else:
                referer = 'https://www.google.com/url?url=%s' % url
            headers = {
                'Referer': referer
            }
            yield scrapy.Request(url, headers=headers)
