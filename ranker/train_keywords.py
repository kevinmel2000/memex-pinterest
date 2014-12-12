# coding: utf-8

import pandas as pd
from jinja2.nodes import Pos

xls = pd.ExcelFile('Keyword_weighting.xlsx')
print xls.sheet_names
df = pd.concat([xls.parse(sheet_name) for sheet_name in xls.sheet_names[1:]])
pos = df.Positive[df.Positive.notnull()]
neg = df.Negative[df.Negative.notnull()]

print pos
print neg
# In[36]:

neg.to_csv('neg.csv', encoding='utf8', index=False)
pos.to_csv('pos.csv', encoding='utf8', index=False)

#get_ipython().system(u'head neg.csv')
