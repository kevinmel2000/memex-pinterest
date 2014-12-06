import os
import re
import urllib
import json
import datetime

import scrapy
from scrapy_memex.utils.url import get_domain
from scrapy.contrib.linkextractors import LinkExtractor
from pharma.items import PharmaItemLoader


def default_data_url(filename):
    return 'file://' + os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            '../../data',
            filename
        )
    )


def setdefaults(dict1, dict2):
    for key, value in dict2.iteritems():
        dict1.setdefault(key, value)


class BaseSearchEngineSpider(scrapy.Spider):

    phrases_url = default_data_url('phrases.json')
    regexes_url = default_data_url('regexes.json')
    max_search_results = 1000
    use_splash = True
    save_html = True
    save_screenshots = True

    def __init__(self, *args, **kwargs):
        super(BaseSearchEngineSpider, self).__init__(*args, **kwargs)
        self.phrases_url = kwargs.get('phrases_url', self.phrases_url)
        self.regexes_url = kwargs.get('regexes_url', self.regexes_url)
        self.use_splash = int(kwargs.get('use_splash', self.use_splash))
        self.save_html = int(kwargs.get('save_html', self.save_html))
        self.save_screenshots = self.use_splash and int(
            kwargs.get('save_screenshots', self.save_screenshots)
        )
        self.max_search_results = int(
            kwargs.get('max_search_results', self.max_search_results)
        )
        if self.use_splash:
            self.splash_meta = {
                'splash': {
                    'html': 1,
                    'png': self.save_screenshots,
                }
            }
        else:
            self.splash_meta = {}

    def start_requests(self):
        phrases_response = urllib.urlopen(self.phrases_url).read()
        self.phrases = json.loads(phrases_response)
        regexes_response = urllib.urlopen(self.regexes_url).read()
        self.regexes = json.loads(regexes_response)

        for phrase in self.phrases:
            for offset in xrange(0, self.max_search_results,
                                 self.search_results_per_page):
                yield self.create_search_request(phrase, offset)

    def create_search_request(self, phrase, offset=0):
        request = self.get_search_request(phrase, offset)
        setdefaults(request.headers, {'Referer': None})
        setdefaults(request.meta, {
            'depth': 0,
            'referers': [],
            'offset': offset,
            'phrase': phrase,
            'skip_broad_crawl_limits': True,
        })
        request.callback = self.parse_search_results
        return request

    def parse_search_results(self, response):
        for request in self.get_search_results_requests(response):
            request.callback = self.parse_external_site
            setdefaults(request.meta, self.splash_meta)
            yield request

    def parse_external_site(self, response):
        yield self._load_webpage_item(response)
        for link in self._extract_links(response):
            yield scrapy.Request(link.url, self.parse_external_site,
                                 meta=self.splash_meta)

    def get_search_request(self, phrase, offset):
        raise NotImplemented

    def get_search_results_requests(self, response):
        raise NotImplemented

    def _extract_links(self, response):
        links = LinkExtractor().extract_links(response)
        return links

    def _load_webpage_item(self, response):
        ld = PharmaItemLoader(response=response)
        ld.add_value('url', response.url)
        ld.add_value('host', get_domain(response.url))
        ld.add_xpath('title', '//title/text()')
        # Temporary storage for png file
        ld.add_value('png', response.meta.get('png'))
        ld.add_value('referers', response.meta.get('referers'))
        ld.add_value('crawled_at', datetime.datetime.utcnow())
        ld.add_value('matched_regexes', self._get_matched_regexes(response))

        if self.save_html:
            ld.add_value('html', response.body_as_unicode())

        if 'link' in response.meta:
            link = response.meta['link']
            ld.add_value('link_text', link.text)
            ld.add_value('link_url', link.url)

        return ld.load_item()

    def _get_matched_regexes(self, response):
        for regex in self.regexes:
            if re.search(regex['regex'], response.body):
                yield regex
