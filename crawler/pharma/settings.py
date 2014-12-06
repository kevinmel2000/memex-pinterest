
BOT_NAME = 'pharma'

SPIDER_MODULES = ['pharma.spiders']
NEWSPIDER_MODULE = 'pharma.spiders'

SPIDER_MIDDLEWARES = {
    'scrapy_memex.spidermiddleware.broadcrawllimits.BroadCrawlLimitsMiddleware': 300,
    'scrapy_memex.spidermiddleware.refererchain.RefererChainMiddleware': 301,
}

DOWNLOADER_MIDDLEWARES = {
    #'scrapy_memex.downloadermiddleware.robotscrawldelay.RobotsCrawlDelayMiddleware': 400,
    'scrapy_memex.downloadermiddleware.splash.SplashMiddleware': 200,
}

ITEM_PIPELINES = {
    'pharma.pipelines.UploadScreenshotsPipeline': 500,
    'pharma.pipelines.UploadHtmlPipeline': 500,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2148.0 Safari/537.36'

DEPTH_LIMIT = 5
REFERER_CHAIN_ENABLED = True

#SPLASH_URL='http://54.69.24.9:8999'

BCL_MAX_INTERNAL_LINKS = 10
BCL_MAX_EXTERNAL_LINKS = 10
BCL_MAX_LINKS_PER_DOMAIN = 100

AWS_ACCESS_KEY_ID = 'AKIAJMNHFYVUTAR5BBMA'
AWS_SECRET_ACCESS_KEY = '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'

S3_SCREENSHOTS_PATH = 's3://darpa-memex/pharma/screenshots/'
S3_HTML_PATH = 's3://darpa-memex/pharma/html/'
