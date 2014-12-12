# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
from sklearn.externals import joblib
import lxml.html.clean
import lxml.html
import lxml.etree
import html2text

def _tree2text(tree):
    cleaner = lxml.html.clean.Cleaner(
        style=True, 
        scripts=True, 
        javascript=True, 
        comments=True, 
        embedded=True, 
        forms=False, 
        page_structure=False,
    )
    
    tree = cleaner.clean_html(tree)
    html = lxml.html.tostring(tree)
    doc = lxml.html.document_fromstring(html)
    return ' '.join(doc.text_content().split())

def prepare_htmltext(html):
    tree = lxml.html.fromstring(html)
    return _tree2text(tree)

def prepare_doc(doc):
    html = doc.get('html_rendered', doc['html'])
    return prepare_htmltext(html.encode('utf8'))

class Ranker(object):

    MODEL = os.path.join(os.path.dirname(__file__), 'models', 'model.joblib')

    def __init__(self, pipe):
        self.pipe = pipe

    @classmethod
    def load(cls, path=MODEL):
        return Ranker(joblib.load(path))

    def score_doc(self, doc):
        X = [prepare_doc(doc)]
        return self.pipe.predict_proba(X)[0][1]

if __name__ == "__main__":
    
    Ranker.load()