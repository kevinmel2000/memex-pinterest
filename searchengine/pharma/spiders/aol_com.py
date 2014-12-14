# -*- coding: utf-8 -*-
import urllib

import scrapy

from pharma.spiders.basesearchengine import BaseSearchEngineSpider


class AolComSpider(BaseSearchEngineSpider):
    name = "aol.com"

    download_delay = 2
    search_results_per_page = 10

    def get_search_request(self, phrase, offset=0):
        encoded_phrase = urllib.quote(phrase.encode('utf-8'))
        url = ('http://search.aol.com/aol/search?q={}&page={}'
               .format(encoded_phrase,
                       offset // self.search_results_per_page + 1))
        return scrapy.Request(url)

    def get_search_results_requests(self, response):
        sel = scrapy.Selector(response)
        for url in sel.css('h3.hac a.find::attr(href)').extract():
            yield scrapy.Request(url)
