from ranker import Ranker
from crawler.discovery.items import WebpageItemLoader
from crawler.discovery.urlutils import (
    add_scheme_if_missing,
    get_domain,
)

from scrapy.spider import Spider
from scrapy.http import Request
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.utils.httpobj import urlparse_cached
from scrapy import log

from datetime import datetime

class TopicalFinder(Spider):
    name = 'topical_finder'

    save_html = True

    def __init__(self, seed_urls, **kwargs):
        # TODO: Implement a random seed mode: e.g. starting from already discovered front pages,
        # but not visited domains
        super(TopicalFinder, self).__init__(**kwargs)
        self.start_urls = [add_scheme_if_missing(url) for url in seed_urls.split(',')]
        self.ranker = Ranker.load()
        self.linkextractor = LinkExtractor()

    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url, is_seed=True)

    def make_requests_from_url(self, url, is_seed=False):
        r = super(TopicalFinder, self).make_requests_from_url(url)
        r.meta['score'] = 0.0
        r.meta['is_seed'] = False

        if is_seed:
            r.meta['is_seed'] = True
            r.meta['score'] = 1.0  # setting maximum score value for seeds
        return r

    def parse(self, response):

        yield self._load_webpage_item(response, is_seed=response.meta['is_seed']).load_item()

        body = response.body_as_unicode().strip().encode('utf8') or '<html/>'
        score = self.ranker.score_html(body)
        log.msg("TC: %s has score=%f" % (response.url, score))
        if score > 0.5:
            for link in self.linkextractor.extract_links(response):
                r = Request(url=link.url)
                r.meta.update(link_text=link.text)
                url_parts = urlparse_cached(r)
                path_parts = url_parts.path.split('/')
                r.meta['score'] = 1.0 / len(path_parts)
                r.meta['is_seed'] = False
                yield r

    def _load_webpage_item(self, response, is_seed):
        depth = response.meta.get('link_depth', 0)
        ld = WebpageItemLoader(response=response)
        ld.add_value('url', response.url)
        ld.add_value('host', get_domain(response.url))
        ld.add_xpath('title', '//title/text()')
        ld.add_value('depth', depth)
        ld.add_value('total_depth', response.meta.get('depth'))
        ld.add_value('crawled_at', datetime.utcnow())
        ld.add_value('is_seed', is_seed)
        ld.add_value('crawler_score', response.meta['score'])

        if self.save_html:
            ld.add_value('html', response.body_as_unicode())  # FIXME: still could be invalid UTF-8

        if 'link' in response.meta:
            link = response.meta['link']
            ld.add_value('link_text', link.text)
            ld.add_value('link_url', link.url)
            ld.add_value('referrer_url', response.meta['referrer_url'])
            ld.add_value('referrer_depth', response.meta['referrer_depth'])
        return ld