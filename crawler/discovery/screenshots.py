# -*- coding: utf-8 -*-
"""
Simple utilities to store screenshots returned by Splash in a folder.
"""
from __future__ import absolute_import

import base64
import os
from hashlib import md5


def save_screenshot(screenshot_dir, prefix, png):
    """
    Save PNG screenshot to a file in ``screenshot_dir`` folder.
    """
    dirname = os.path.join(screenshot_dir, prefix)
    makedir(dirname)

    fn = os.path.join(dirname, md5(png).hexdigest() + '.png')
    with open(fn, 'wb') as fp:
        fp.write(png)
    return fn


def makedir(path):
    """ Mane sure the folder exists """
    try:
        os.makedirs(path)
    except OSError:
        pass


