# -*- coding: utf-8 -*-

# Scrapy settings for crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'discovery'
SPIDER_MODULES = ['discovery.spiders']
NEWSPIDER_MODULE = 'discovery.spiders'

DOWNLOADER_MIDDLEWARES = {
    'discovery.robots_mw.RobotsCrawlDelayMiddleware': 100,
    'discovery.splash_ext.SplashMiddleware': 950,
}
ROBOTS_CRAWLDELAY_ENABLED = True
AUTOTHROTTLE_ENABLED = False  # it doesn't play well with RobotsCrawlDelayMiddleware
DUPEFILTER_CLASS = 'discovery.splash_ext.SplashAwareDupeFilter'  # needed by SplashMiddleware
HTTPCACHE_STORAGE = 'discovery.splash_ext.SplashAwareFSCacheStorage'  # needed by SplashMiddleware
SPLASH_URL = 'http://127.0.0.1:8050'
SPLASH_PROXY_URL = 'http://127.0.0.1:8051'

HTTPCACHE_ENABLED = True

MEMUSAGE_ENABLED = True
DEPTH_STATS_VERBOSE = True
DEPTH_PRIORITY = True
DEPTH_LIMIT = 6  # make sure to adjust this when changing depth-related spider attributes
AJAXCRAWL_ENABLED = True
DOWNLOAD_TIMEOUT = 20  # default was 180s
REDIRECT_MAX_TIMES = 10  # default was 20
CLOSESPIDER_ITEMCOUNT = 1000  # ~100 websites max; don't crawl the whole Internet
DOWNLOAD_DELAY = 1
DUPEFILTER_DEBUG = True

import logging
logging.getLogger("tldextract").setLevel(logging.INFO)

#USER_AGENT = 'crawler (+http://www.yourdomain.com)'
