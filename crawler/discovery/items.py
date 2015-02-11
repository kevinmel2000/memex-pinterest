import scrapy
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Compose


class WebpageItem(scrapy.Item):
    mongo_collection = 'urlinfo'

    url = scrapy.Field()  # url of a page
    host = scrapy.Field()  # website
    title = scrapy.Field()  # <title> contents
    depth = scrapy.Field()  # depth at which the page is found, relative to its website
    referrer_depth = scrapy.Field()  # depth of the referrer page
    total_depth = scrapy.Field()  # number of hops from a seed page
    crawled_at = scrapy.Field()  # datetime in UTC
    html = scrapy.Field()  # full HTML
    html_rendered = scrapy.Field()  # full HTML rendered via Splash, optional
    link_text = scrapy.Field()  # text of the link that lead to this page
    link_url = scrapy.Field()  # URL of a link that lead to this page
    referrer_url = scrapy.Field()  # URL of a referrer page
    is_seed = scrapy.Field()  # this is True for pages from seed websites
    screenshot_path = scrapy.Field()
    # score = scrapy.Field()


class WebpageItemLoader(ItemLoader):
    default_item_class = WebpageItem
    default_output_processor = TakeFirst()
    link_text_in = MapCompose(unicode, unicode.strip)
    title_out = Compose(TakeFirst(), unicode.strip)