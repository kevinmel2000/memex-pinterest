import os
from scrapy.utils.conf import closest_scrapy_cfg


def project_root():
    return os.path.dirname(closest_scrapy_cfg())
