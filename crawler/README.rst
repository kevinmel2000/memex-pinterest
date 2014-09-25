Scrapy Spiders
==============

"discovery" folder contains a Scrapy project with a spider 
that accepts a list of seed URLs and finds linked external websites.
 
Installation
------------

1. Install all requirements from requirements.txt;
2. install and run Splash_ - some instructions 
   are `here <http://splash.readthedocs.org/en/latest/install.html>`__.

.. _Splash: https://github.com/scrapinghub/splash

Usage
-----

From Console
~~~~~~~~~~~~

To try it run

::
    
    scrapy crawl website_finder -a seed_urls=myurl.com -s SPLASH_URL=<YOUR_SPLASH_ADDRESS> -o data.csv

Check `discovery/spiders/website_finder.py <https://github.com/acaceres2176/memex-hackathon-1/blob/master/crawler/discovery/spiders/website_finder.py>`_ 
for more info.

API
~~~

To expose HTTP API run ``scrapyd`` from this folder. 
This is required for UI to work.
