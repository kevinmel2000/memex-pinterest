# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import scrapy
import hashlib
from scrapy.contrib.spiders import CSVFeedSpider
from discovery.urlutils import add_scheme_if_missing


class HtmlSpider(CSVFeedSpider):
    name = 'html'
    headers = ['url']
    out_dir = 'data/train/neg'
    start_urls = ['file:///Users/kmike/scrap/memex-hackathon-1/crawler/notebooks/neg.csv']

    def parse_row(self, response, row):
        url = add_scheme_if_missing(row['url'])
        return scrapy.Request(url, self.parse_website, meta={'url': url})

    def parse_website(self, response):
        fn = os.path.join(self.out_dir, hashlib.md5(response.url).hexdigest()) + '.html'
        with open(fn, 'wb') as f:
            f.write(response.body)
