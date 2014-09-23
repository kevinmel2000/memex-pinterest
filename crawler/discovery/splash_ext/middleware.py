# -*- coding: utf-8 -*-
from __future__ import absolute_import
import logging
from scrapy import log


class SplashMiddleware(object):
    """
    Scrapy downloader middleware that passes requests through Splash_
    when 'splash' Request.meta key is set.

    To enable the middleware add it to settings::

        DOWNLOADER_MIDDLEWARES = {
            'splash_mw.SplashMiddleware': 950,
        }

    and then use ``splash`` meta key to pass options::

        yield Request(url, self.parse_result, meta={'splash': {
            # use render.json options here
            'html': 1,
            'png': 1,
        }}

    The response

    .. _Splash: https://github.com/scrapinghub/splash

    """
    DEFAULT_PROXY_URL = 'http://127.0.0.1:8051'
    SPLASH_EXTRA_TIMEOUT = 5

    def __init__(self, crawler, proxy_url):
        self.crawler = crawler
        self.proxy_url = proxy_url

    @classmethod
    def from_crawler(cls, crawler):
        proxy_url = crawler.settings.get('SPLASH_PROXY_URL', cls.DEFAULT_PROXY_URL)
        return cls(crawler, proxy_url)

    def process_request(self, request, spider):
        # FIXME: https is not supported because Splash doesn't support it
        # in proxy mode. Switch to render.json, don't bother with headers
        # and take care of download slots ourselves?

        splash_options = request.meta.get('splash')
        if not splash_options:
            return

        if request.method != 'GET':
            log.msg("Only GET requests are supported by SplashMiddleware; %s will be handled without Splash" % request, logging.WARNING)
            return request

        for key, value in splash_options.items():
            if key.lower() == 'timeout':
                request.meta['download_timeout'] = max(
                    request.meta.get('download_timeout', 1e6),
                    float(value) + self.SPLASH_EXTRA_TIMEOUT
                )
            request.headers['X-Splash-%s' % key] = value

        request.meta['proxy'] = self.proxy_url
        self.crawler.stats.inc_value('splash/request_count')
