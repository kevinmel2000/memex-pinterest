# -*- coding: utf-8 -*-
from __future__ import absolute_import
import hashlib
from scrapy.dupefilter import RFPDupeFilter
from scrapy.utils.request import request_fingerprint


def splash_requst_fingerprint(request, include_headers=None):
    """ Request fingerprint that takes 'splash' meta key into account """

    fp = request_fingerprint(request, include_headers=include_headers)
    if 'splash' not in request.meta:
        return fp

    h = hashlib.sha1(fp)
    for key, value in sorted(request.meta['splash'].items()):
        h.update(key)
        h.update(str(value))
    return h.hexdigest()


class SplashAwareDupeFilter(RFPDupeFilter):
    """
    DupeFilter that takes 'splash' meta key in account.
    It should be used with SplashMiddleware.
    """

    def request_fingerprint(self, request):
        return splash_requst_fingerprint(request)
