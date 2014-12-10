# -*- coding: utf-8 -*-
import urllib

import scrapy

from pharma.spiders.basesearchengine import BaseSearchEngineSpider


class BingComSpider(BaseSearchEngineSpider):
    name = "bing.com"

    download_delay = 2
    search_results_per_page = 10

    def get_search_request(self, phrase, offset=0):
        encoded_phrase = urllib.quote(phrase.encode('utf-8'))
        url = ('http://www.bing.com/search?q={}&first={}'
               .format(encoded_phrase, offset))
        return scrapy.Request(url)

    def get_search_results_requests(self, response):
        sel = scrapy.Selector(response)
        for url in sel.css(
            'ol#b_results h2 a[href^="http"]::attr(href)'
        ).extract():
            yield scrapy.Request(url)
