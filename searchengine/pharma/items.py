# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst
from scrapy.contrib.loader.processor import MapCompose
from scrapy.contrib.loader.processor import Compose
from scrapy.contrib.loader.processor import Identity


class WebpageItem(scrapy.Item):
    url = scrapy.Field()  # url of a page
    host = scrapy.Field()  # website
    title = scrapy.Field()  # <title> contents
    depth = scrapy.Field()  # depth at which the page is found relative to site
    total_depth = scrapy.Field()  # number of hops from a seed page
    crawled_at = scrapy.Field()  # datetime in UTC
    html = scrapy.Field()  # full HTML
    html_rendered = scrapy.Field()  # full HTML rendered via Splash, optional
    link_text = scrapy.Field()  # text of the link that lead to this page
    link_url = scrapy.Field()  # URL of a link that lead to this page
    is_seed = scrapy.Field()  # this is True for pages from seed websites
    png = scrapy.Field()  # temporary field for storing raw png screenshot
    screenshot_url = scrapy.Field()
    screenshot_path = scrapy.Field()
    html_url = scrapy.Field()


class WebpageItemLoader(ItemLoader):
    default_item_class = WebpageItem
    default_output_processor = TakeFirst()
    link_text_in = MapCompose(unicode, unicode.strip)
    title_out = Compose(TakeFirst(), unicode.strip)


class PharmaItem(WebpageItem):
    referers = scrapy.Field()
    matched_regexes = scrapy.Field()


class PharmaItemLoader(WebpageItemLoader):
    default_item_class = PharmaItem
    referers_out = Identity()
