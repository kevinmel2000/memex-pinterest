
# coding: utf-8

# In[89]:

import sys
sys.path.insert(0, '../../')

import os
import glob
import numpy as np
import lxml.html.clean
import lxml.html
import lxml.etree
import html2text
from tqdm import tqdm
from ui.mongoutils.memex_mongo_utils import MemexMongoUtils

from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.cross_validation import train_test_split, cross_val_score
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

from ranker import Ranker

def get_informative_features(vectorizer, clf, class_labels, N):
    """
    Return text with features with the highest
    absolute coefficient values, per class.
    """
    feature_names = vectorizer.get_feature_names()
    features_by_class = []
    for i, class_label in enumerate(class_labels):
        topN = np.argsort(clf.coef_[i])[-N:]
        bottomN = np.argsort(clf.coef_[i])[:N]
        res = []
        for j in reversed(topN):
            coef = clf.coef_[i][j]
            if coef > 0:
                res.append("%0.6f: %s" % (coef, feature_names[j]))
        for j in reversed(bottomN):
            coef = clf.coef_[i][j]
            if coef < 0:
                res.append("%0.6f: %s" % (coef, feature_names[j]))
        features_by_class.append((class_label, '\n'.join(res)))
    return features_by_class


def get_informative_features_binary(vec, clf, top):
    """
    Return text with features with highest absolute coefficient values
    (for a binary classification task).
    """
    return dict(get_informative_features(vec, clf, [0], top))[0]


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


def prepare_html(fn):
    with open(fn, 'rb') as f:
        tree = lxml.html.parse(f)
        
    return _tree2text(tree)


def load_documents(pat):    
    for fn in tqdm(glob.glob(pat), leave=True):
        try:
            yield prepare_html(fn)
        except Exception as e:
            print("error processing %s: %s" % (fn, e))
            
def posneg2xy(pos, neg):
    X = pos + neg
    y = [True]*len(pos) + [False]*len(neg)
    return X, y

def get_mdocs(interest):
    
    mmu = MemexMongoUtils()
    return mmu.list_all_urls_with_interest(interest, return_html = True)

def prepare_doc(doc):
    html = doc.get('html_rendered', doc['html'])
    return prepare_htmltext(html.encode('utf8'))

def train_on_user_input():

    #docs_pos = list(load_documents('../data/train/pos/*.html'))
    #docs_neg = list(load_documents('../data/train/neg/*.html'))
    
    #X_Amanda, y_Amanda = posneg2xy(docs_pos, docs_neg)
    #X_Amanda, y_Amanda = posneg2xy(docs_pos, [])
    
    docs_mongo_pos = [prepare_doc(doc) for doc in get_mdocs(True)]
    docs_mongo_neg = [prepare_doc(doc) for doc in get_mdocs(False)]
    
    print "Positive examples: " + str(len(docs_mongo_pos))
    print "Negative examples: " + str(len(docs_mongo_neg))
    
    X_mongo, y_mongo = posneg2xy(docs_mongo_pos, docs_mongo_neg)
    
    #X = X_Amanda + X_mongo
    #y = y_Amanda + y_mongo
    X = X_mongo
    y = y_mongo    
    
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    
    vec = CountVectorizer(min_df=2, ngram_range=(1,2)) #, stop_words='english')
    clf = LogisticRegression(C=0.1, penalty='l2')
    
    pipe = Pipeline([
        ('vec', vec),
        ('clf', clf),
    ])
    
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)
    print classification_report(y_test, y_pred)
        
    cross_val_score(pipe, np.array(X), np.array(y), cv=10, scoring='f1').mean()
    try:
        print get_informative_features_binary(vec, clf, 200)
    except:
        print "Couldn't print all informative features, but scoring anyway"
        
    pipe.fit(X, y)
    
    MODEL = os.path.join(os.path.dirname(__file__), 'models', 'model.joblib')    
    joblib.dump(pipe, MODEL, compress=1)
    #get_ipython().system(u"ls -lh '../../ranker/models/'")
    
#    ranker = Ranker.load()
#    ranker.score_doc(get_mdocs(True)[4])
    
