from urlparse import urlparse
from scrapy.conf import settings

class OnionProxyMiddleware(object):

    def process_request(self, request, spider):
        host = urlparse(request.url).netloc
        if ":" in host:
            host = host.split(":")[0]

        if host.endswith(".onion"):
            request.meta["proxy"] = settings.get("ONION_HTTP_PROXY")