# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
from scrapy.contrib.httpcache import FilesystemCacheStorage
from .dupefilter import splash_requst_fingerprint


class SplashAwareFSCacheStorage(FilesystemCacheStorage):
    def _get_request_path(self, spider, request):
        key = splash_requst_fingerprint(request)
        return os.path.join(self.cachedir, spider.name, key[0:2], key)
