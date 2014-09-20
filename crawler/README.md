Scrapy Spiders
==============

"discovery" folder contains a Scrapy project with a spider 
that accepts a list of seed URLs and finds linked external websites. 

To try it, install all requirements from requirements.txt and run

    scrapy crawl website_finder -a seed_urls=myurl.com -o data.csv

Check `discovery/spiders/website_finder.py` for more info.
