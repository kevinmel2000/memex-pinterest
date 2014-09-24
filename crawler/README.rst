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

To try it,  and run

    scrapy crawl website_finder -a seed_urls=myurl.com -s SPLASH_URL=<YOUR_SPLASH_ADDRESS> -o data.csv

Check :file:`discovery/spiders/website_finder.py` for more info.
