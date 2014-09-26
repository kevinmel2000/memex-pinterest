# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
from sklearn.externals import joblib
from html import prepare_mongodoc


class Ranker(object):

    MODEL = os.path.join(os.path.dirname(__file__), 'models', 'model.joblib')

    def __init__(self, pipe):
        self.pipe = pipe

    @classmethod
    def load(cls, path=MODEL):
        return Ranker(joblib.load(path))

    def score_doc(self, doc):
        X = [prepare_mongodoc(doc)]
        return self.pipe.predict_proba(X)[0][1]
