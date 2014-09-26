# -*- coding: utf-8 -*-
from __future__ import absolute_import
import lxml.html
import lxml.html.clean


cleaner = lxml.html.clean.Cleaner(
    style=True,
    scripts=True,
    javascript=True,
    comments=True,
    embedded=True,
    forms=True,
    page_structure=False,
)


def tree2text(tree):
    tree = cleaner.clean_html(tree)
    html = lxml.html.tostring(tree)
    doc = lxml.html.document_fromstring(html)
    return ' '.join(doc.text_content().split())


def prepare_html(html):
    tree = lxml.html.fromstring(html)
    return tree2text(tree)


def prepare_mongodoc(doc):
    html = doc.get('html_rendered', doc.get('html')) or ''
    return prepare_html(html.encode('utf8'))


def prepare_htmlfile(fn):
    with open(fn, 'rb') as f:
        tree = lxml.html.parse(f)

    return tree2text(tree)
