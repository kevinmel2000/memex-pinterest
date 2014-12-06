import time
from urlparse import urlparse
from base64 import urlsafe_b64encode

from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.internet.threads import deferToThread
import boto


time_str = time.strftime('%Y%m%d%H%M%S')


class S3Pipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        u = urlparse(self.uri)
        bucketname = u.hostname
        access_key = u.username or settings['AWS_ACCESS_KEY_ID']
        secret_key = u.password or settings['AWS_SECRET_ACCESS_KEY']
        conn = boto.connect_s3(access_key, secret_key)
        self.root = u.path
        self.bucket = conn.get_bucket(bucketname, validate=False)

    def store(self, keyname, data):
        return deferToThread(self._store, keyname, data)

    def _store(self, keyname, data):
        key = self.bucket.new_key(keyname)
        key.set_contents_from_string(data)
        key.set_acl('public-read')
        key.close()
        url = key.generate_url(expires_in=0, query_auth=False)
        return url


class UploadScreenshotsPipeline(S3Pipeline):

    def __init__(self, settings):
        self.uri = settings.get('S3_SCREENSHOTS_PATH')
        super(UploadScreenshotsPipeline, self).__init__(settings)

    @inlineCallbacks
    def process_item(self, item, spider):
        png = item.get('png')
        if png is None:
            returnValue(item)

        keyname = '%s/%s/%s/%s' % (
            self.root, spider.name, time_str,
            urlsafe_b64encode(item['url']) + '.png'
        )
        url = yield self.store(keyname, png)
        del item['png']
        item['screenshot_url'] = url
        returnValue(item)


class UploadHtmlPipeline(S3Pipeline):
    def __init__(self, settings):
        self.uri = settings.get('S3_HTML_PATH')
        super(UploadHtmlPipeline, self).__init__(settings)

    @inlineCallbacks
    def process_item(self, item, spider):
        if 'html' not in item:
            returnValue(item)
        html_utf8 = item['html'].encode('utf-8')
        filename = urlsafe_b64encode(item['url']) + '.html'
        keyname = '%s/%s/%s/%s' % (
            self.root, spider.name, time_str, filename
        )
        url = yield self.store(keyname, html_utf8)
        del item['html']
        item['html_url'] = url
        returnValue(item)
