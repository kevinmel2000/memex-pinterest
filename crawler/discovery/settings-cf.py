BOT_NAME = 'discovery'
SPIDER_MODULES = ['discovery.spiders']
NEWSPIDER_MODULE = 'discovery.spiders'

SPIDER_MIDDLEWARES = {
    'crawlfrontier.contrib.scrapy.middlewares.schedulers.SchedulerSpiderMiddleware': 1000,
}

DOWNLOADER_MIDDLEWARES = {
    'discovery.robots_mw.RobotsCrawlDelayMiddleware': 100,
    'discovery.randomua_mw.RandomUserAgentMiddleware' : 250,
    'crawlfrontier.contrib.scrapy.middlewares.schedulers.SchedulerDownloaderMiddleware': 500,
    'discovery.splash_ext.SplashMiddleware': 950,
    'discovery.proxy_mw.OnionProxyMiddleware' : 1000,
}

USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0) Gecko/16.0 Firefox/16.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10'
]

ONION_HTTP_PROXY = 'http://sourcetor:8123'

ROBOTS_CRAWLDELAY_ENABLED = True
AUTOTHROTTLE_ENABLED = False  # it doesn't play well with RobotsCrawlDelayMiddleware
DUPEFILTER_CLASS = 'discovery.splash_ext.SplashAwareDupeFilter'  # needed by SplashMiddleware
HTTPCACHE_STORAGE = 'discovery.splash_ext.SplashAwareFSCacheStorage'  # needed by SplashMiddleware
SPLASH_URL = 'http://splash:8050'
SPLASH_PROXY_URL = 'http://splash:8051'

MONGO_URI = "localhost:27017"
MONGO_DATABASE = 'MemexHack'
#ITEM_PIPELINES = {
#    'discovery.pipelines.SourcePinPipeline': 100,
#}

HTTPCACHE_ENABLED = True

MEMUSAGE_ENABLED = True
DEPTH_STATS_VERBOSE = True
DEPTH_PRIORITY = True
DEPTH_LIMIT = 3  # make sure to adjust this when changing depth-related spider attributes
AJAXCRAWL_ENABLED = True
DOWNLOAD_TIMEOUT = 60  # default was 180s
REDIRECT_MAX_TIMES = 5  # default was 20
CLOSESPIDER_ITEMCOUNT = 300  # ~100 websites max; don't crawl the whole Internet
DOWNLOAD_DELAY = 1
DUPEFILTER_DEBUG = True

import logging
logging.getLogger("tldextract").setLevel(logging.INFO)

#USER_AGENT = 'crawler (+http://www.yourdomain.com)'

FRONTIER_SETTINGS = 'discovery.frontier.settings'
SCHEDULER = 'crawlfrontier.contrib.scrapy.schedulers.frontier.CrawlFrontierScheduler'

# TODO concurrency and performance