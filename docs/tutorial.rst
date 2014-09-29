********
Tutorial
********

.. toctree::
   :maxdepth: 2


Install
=======

SourcePin is easy to install, here are the steps.

* Install dependencies ::

    sudo apt-get install mongodb
    sudo apt-get install libxml2-dev libxslt1-dev python-dev
    sudo apt-get build-dep python-lxml
    pip install pymongo
    pip install scrapy
    pip install scrapyd
    pip install splash
    pip install python-scrapyd-api
    pip install lxml
    pip install service_identity
    pip install pytest
    pip install tldextract
    pip install reppy
    pip install scrapy-inline-requests

If any of the previous commands fail, please see the documentation 
for each respective project or email acaceres@hyperiongray.com for help 
(Splash in particular can cause some trouble).

Once dependencies have been installed please check out the SourcePin code by doing ::

    git@github.com:acaceres2176/memex-hackathon-1.git
    
If you don't have access to this repo please email acaceres@hyperiongray.com.

Once dependencies are installed and the code is checked out head on over to the scrapy crawler
"discovery" crawler directory, from the project root: ::

    cd crawler
    scrapyd
    
This will start scrapyd on your local machine on port 6800. Next, start the Splash server by doing ::

    python -m splash.server

This will start splash on your local machine.

Almost there... now it's time to configure the server application, pop open *ui/settings.py*. The only
config value that you really need to worry about is ::

   SCREENSHOT_DIR = '/home/memex-punk/memex-dev/workspace/memex-pinterest/ui/static/images/screenshots'

Replace the above with the equivalent directory on your filesystem, for example yours may be *'/home/your-user/memex-hackathon-1/ui/static/images/screenshots'*.

Now you're ready to start the SourcePin application,
from the project root ::

   python server.py
    
Now open up your web browser and go to http://localhost:5000. You should see a blank page with
the Hyperion Gray SourcePin title at the top.

Now it's time to instantiate the database. You can do this by doing the following from the project root ::

    cd ui/mongoutils
    python memex_mongo_utils.py

You should see some messages that the db is being instantiated, and you're good to go!

Using the UI
============

In the base install the UI provides 2 important interfaces. The first is the ability to provide 
a seed URL, which performs crawls and the other an interface to view these results to make a decision
on their relevance to your particular interest set.

To get started click over to the Crawl New Sites tab, it should look like this:

.. image:: _static/crawl-new.png
    :width: 800px
    :align: center
    :height: 400px
    :alt: Crawl a new website from here
    
Enter a website that you want to seed from in the box and click Submit. You should see the website
inerted into a table on the screen and go into a state of "Running". At this point, the site has
been sent to our Scrapy based crawler, is being crawled and screenshotted, and being inserted into
the database. Feel free to test this out on http://www.hyperiongray.com/ at your leisure. It should
look like this:

.. image:: _static/running-crawl.png
    :width: 800px
    :align: center
    :height: 400px
    :alt: A running crawl

Once you've entered some seeds in there, the system is crawling using Scrapy/Scrapyd, sending web pages
to be rendered in a WebKit browser using Splash, and storing information in the database. To browse the
results, check out the View Crawl Data link. It should look like this:
    
.. image:: _static/success-crawl.png
    :width: 800px
    :align: center
    :height: 400px
    :alt: Viewing successful crawl data

Once you are viewing the crawl data successfully, you can drill down on specific hosts. In doing so
you'll open a "URL-level view" of the data. You should see screenshots of individual pages associated
with a host. You can then mark interest or disinterst in them. This information gets stored in the database
and can be used as generic user feedback and training data when plugging in to the scoring API.

Using the API
=============

SourcePin has a simple, but powerful API that allows you to submit sites for crawl, view all results,
and plug in to the scoring mechanism. It's pretty sweet. Please note that you have to explicitly request
JSON by using the Accept HTTP header value application/json. Here's how it works.

Endpoint **/hosts/<page>**
**************************

Purpose: Retrieve host-level data.

Example call ::

   curl -iH "Accept: application/json" http://localhost:5000/hosts/1

Example response ::

   [
   	{
   		"host_score": 0,
   		"host": "hyperiongray.com",
   		"hsu_screenshot_path": null,
   		"num_urls": 2
   	},
   
   	{
   		"host_score": 0,
   		"host": "stackoverflow.com",
   		"hsu_screenshot_path": null,
   		"num_urls": 28
   	},
   
   	{
   		"host_score": 0,
   		"host": "hyperiongray.com",
   		"hsu_screenshot_path": null,
   		"num_urls": 2
   	},
   
   	{
   		"host_score": 0,
   		"host": "stackoverflow.com",
   		"hsu_screenshot_path": null,
   		"num_urls": 29
   	}
   ]

Endpoint **/urls/<page>**
*************************

Purpose: Retrieve url-level data.

Example call ::

   curl -iH "Accept: application/json" http://localhost:5000/urls/1

Example response ::

   [
      {
         "referrer_url": "http://stackoverflow.com/questions/6504810/how-to-install-lxml-on-ubuntu/",
         "total_depth": 1,
         "crawled_at": "2014-09-29T02:04:52.593000",
         "title": "User AKX - Stack Overflow",
         "url": "http://stackoverflow.com/users/51685/akx",
         "link_url": "http://stackoverflow.com/users/51685/akx",
         "referrer_depth": 0,
         "depth": 1,
         "is_seed": true,
         "host": "stackoverflow.com",
         "html" : "<big long html string>",
         "rendered_html" : "<big long html string after browser rendering>"
      },
   
      {
         "referrer_url": "http://stackoverflow.com/questions/6504810/how-to-install-lxml-on-ubuntu/",
         "total_depth": 1,
         "crawled_at": "2014-09-29T02:04:53.488000",
         "title": "python - Error installing libxml2-dev on Ubuntu 9.10 - for lxml-etree - Stack Overflow",
         "url": "http://stackoverflow.com/questions/14024229/error-installing-libxml2-dev-on-ubuntu-9-10-for-lxml-etree",
         "link_url": "http://stackoverflow.com/questions/14024229/error-installing-libxml2-dev-on-ubuntu-9-10-for-lxml-etree",
         "link_text": "Error installing libxml2-dev on Ubuntu 9.10 - for lxml-etree",
         "referrer_depth": 0,
         "depth": 1,
         "is_seed": true,
         "host": "stackoverflow.com",
         "html" : "<big long html string>",
         "rendered_html" : "<big long html string after browser rendering>"
      },
   
      {
         "referrer_url": "http://stackoverflow.com/questions/6504810/how-to-install-lxml-on-ubuntu/",
         "total_depth": 1,
         "crawled_at": "2014-09-29T02:04:54.759000",
         "title": "User JimmyYe - Stack Overflow",
         "url": "http://stackoverflow.com/users/1266258/jimmyye",
         "link_url": "http://stackoverflow.com/users/1266258/jimmyye",
         "referrer_depth": 0,
         "depth": 1,
         "is_seed": true,
         "host": "stackoverflow.com",
         "html" : "<big long html string>",
         "rendered_html" : "<big long html string after browser rendering>"
      }
   ]
   
   
Endpoint: **/schedule-spider/**
*******************************

Purpose: Schedule the spider to run against a URL.

Example call ::

   curl -iH http://localhost:5000/schedule-spider/?url='https://docs.python.org/2/library/datetime.html'

Example response (headers included below) ::

   HTTP/1.0 200 OK
   Content-Type: text/html; charset=utf-8
   Content-Length: 2
   Server: Werkzeug/0.9.6 Python/2.7.6
   Date: Mon, 29 Sep 2014 17:24:03 GMT
   
   OK

Endpoint: **/url-job-state/**, **params: url**
**********************************************

Purpose: Check the job state of a spider instantiated against a URL.

Example call ::

   curl -iH http://localhost:5000/url-job-state/?url='https://docs.python.org/2/library/datetime.html'

Example response (headers included below) ::

   HTTP/1.0 200 OK
   Content-Type: text/html; charset=utf-8
   Content-Length: 7
   Server: Werkzeug/0.9.6 Python/2.7.6
   Date: Mon, 29 Sep 2014 17:26:32 GMT
   
   Running

Note: The above can be in a state of Inititalizing, Running or Done

Endpoint **/mark-interest/<true|false>/**, **params: url**
**********************************************************

Purpose: Mark interest in a URL, store this information

Example call ::   

   curl http://localhost:5000/mark-interest/true/?url='https://docs.python.org/2/library/datetime.html'

Example response (headers included below) ::

   HTTP/1.0 200 OK
   Content-Type: text/html; charset=utf-8
   Content-Length: 2
   Server: Werkzeug/0.9.6 Python/2.7.6
   Date: Mon, 29 Sep 2014 17:31:10 GMT
   
   OK

Endpoint **/set-score/<score>**, **params: url**
************************************************

**Note: <score> is an integer from 1-100**

Purpose: After performing some analysis, set the score of a URL, the UI organizes by score and stores this
value in subsequent requests for URLs. For requesting hosts, the score is set automatically as the highest
scoring URL in the set, this may change later.

Example call ::

   curl http://localhost:5000/set-score/83/?url='https://docs.python.org/2/library/datetime.html'
   
Example response ::

   HTTP/1.0 200 OK
   Content-Type: text/html; charset=utf-8
   Content-Length: 2
   Server: Werkzeug/0.9.6 Python/2.7.6
   Date: Mon, 29 Sep 2014 17:51:38 GMT
   
   OK


Writing an analysis plugin
==========================

Analysis plugins should simply use the REST API to add scoring to URLs in the system. Assume that URLs
have already been added to the system either via scheduled crawling using hte UI or API. Let's take a concrete 
(if a little contrived) example. Say we want to score all URLs based on the wordcount of the rendered
HTML. One could simply make a call to the **/host/0** endpoint to list the first page of hosts, iterating
through these pages will give you a list of all hosts. These can then be passed to the **/urls/<host>** endpoint
to get the URLs, their html, and their rendered HTML. Once you have these, you can run them through a simple wordcount  
function, normalizing the score to be between 0 and 100, and then index the score by using the **/set-score/<score>**
endpoint. If this is unclear or you want to use this but something isn't working properly, please email acaceres@hyperiongray.com.

Troubleshooting
===============

* If you enter a URL to crawl, click submit and nothing happens then something has gone terribly wrong in your setup or there is a bug in the application. Check the terminal where you are running server.py, it should contain a traceback. 

* If you get a 500 internal server error, or submitting something seems to act funny (or do nothing) check the terminal where you are running server.py, it should contain a traceback.

* If you get a 404 not found, that usually means you've messed up an API call, check these docs and make sure you have the proper fields and parameters set.

In any case email acaceres@hyperiongray.com for help, and copy and paste
any relevant exception traceback information if possible. This can usually be found in the terminal in which you are running
server.py.

Thanks
======

Thanks for trying out our stuff, feedback is always welcome!