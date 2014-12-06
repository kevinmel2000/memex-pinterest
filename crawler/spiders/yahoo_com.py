# -*- coding: utf-8 -*-
import re
import urllib

import scrapy

from pharma.spiders.basesearchengine import BaseSearchEngineSpider


class YahooComSpider(BaseSearchEngineSpider):
    name = "yahoo.com"

    download_delay = 2
    search_results_per_page = 10

    def get_search_request(self, phrase, offset=0):
        encoded_phrase = urllib.quote(phrase.encode('utf-8'))
        url = ('https://search.yahoo.com/search?p={}&b={}'
               .format(encoded_phrase,
                       offset + 1))
        return scrapy.Request(url)

    def get_search_results_requests(self, response):
        sel = scrapy.Selector(response)
        for link in sel.css('h3 a[id^="link-"]::attr(href)').extract():
            url_match = re.search('/RU=([^/]+)', link)
            if url_match:
                url = urllib.unquote_plus(url_match.group(1))
                yield scrapy.Request(url)
            else:
                self.log('External url not found on: {}'.format(link))
