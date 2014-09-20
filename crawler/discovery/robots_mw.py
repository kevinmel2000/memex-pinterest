# -*- coding: utf-8 -*-
from __future__ import absolute_import
import logging
import urlparse

from reppy.parser import Rules

from scrapy import log
from scrapy.exceptions import NotConfigured
from scrapy.http import Request
from scrapy.utils.httpobj import urlparse_cached


def get_robotstxt_url(url):
    """
    >>> get_robotstxt_url("https://example.com/foo/bar?baz=1")
    'https://example.com/robots.txt'
    """
    if not isinstance(url, urlparse.ParseResult):
        url = urlparse.urlparse(url)
    return "%s://%s/robots.txt" % (url.scheme, url.netloc)


class RobotRules(Rules):
    def delay(self, agent=None):
        """
        How fast can the specified agent legally crawl this site?
        If no agent is given, try '*' first; if there is no rule for '*'
        return a minimum allowed value among all the agents.
        If there are no matching Crawl-Delay directives return None.
        """
        if agent is not None:
            return super(RobotRules, self).delay(agent)

        delay = super(RobotRules, self).delay("*")
        if delay is not None:
            return delay

        return self.get_min_delay(map(self.delay, self.agents))

    @classmethod
    def get_min_delay(cls, delays):
        """
        >>> RobotRules.get_min_delay([0.5, 1.2])
        0.5
        >>> RobotRules.get_min_delay([None, 3, 2])
        2
        >>> RobotRules.get_min_delay([])
        >>> RobotRules.get_min_delay([None])
        """
        delays = [d for d in delays if d is not None]
        if not delays:
            return None
        return min(delays)


class RobotsCrawlDelayMiddleware(object):
    """
    Scrapy downloader middleware that makes spiders respect
    Crawl-Delay from robots.txt.

    Settings to enable this middleware::

        DOWNLOADER_MIDDLEWARES = {
            'robots_mw.RobotsCrawlDelayMiddleware': 100,
        }
        ROBOTS_CRAWLDELAY_ENABLED = True

        # currently autothrottle doesn't play well with RobotsCrawlDelayMiddleware
        AUTOTHROTTLE_ENABLED = False

    """

    DOWNLOAD_PRIORITY = 1000
    MAX_DOWNLOAD_DELAY = 100

    def __init__(self, crawler):
        if not crawler.settings.getbool('ROBOTS_CRAWLDELAY_ENABLED'):
            raise NotConfigured

        self.crawler = crawler
        self._robot_rules = {}  # domain => robots.txt rules object

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        rules = self.robotstxt(request, spider)
        self._adjust_delay(rules, request, spider)

    def robotstxt(self, request, spider):
        url = urlparse_cached(request)
        if url.netloc not in self._robot_rules:
            self._robot_rules[url.netloc] = None
            req = Request(get_robotstxt_url(url), priority=self.DOWNLOAD_PRIORITY)
            dfd = self.crawler.engine.download(req, spider)
            dfd.addCallback(self._parse_robots, spider=spider)
        return self._robot_rules[url.netloc]

    def _parse_robots(self, response, spider):
        if response.status != 200:
            return

        rules = RobotRules(
            url=response.url,
            status=response.status,
            content=response.body_as_unicode(),
            expires=None
        )
        self._robot_rules[urlparse_cached(response).netloc] = rules
        self._adjust_delay(rules, response, spider)

    def _adjust_delay(self, rules, request_or_response, spider):
        if rules is None:
            return

        robots_delay = rules.delay()
        if robots_delay is None:
            return

        key, slot = self._get_slot(request_or_response, spider)

        delay = min(max(slot.delay, robots_delay), self.MAX_DOWNLOAD_DELAY)
        if delay != slot.delay:
            log.msg("Adjusting delay for %s: %0.2f -> %0.2f" % (key, slot.delay, delay), logging.DEBUG)
            slot.delay = delay
            self.crawler.stats.set_value('robots.txt/crawl-delay/%s' % key, delay)

    def _get_slot(self, request_or_response, spider):
        return self.crawler.engine.downloader._get_slot(request_or_response, spider)
