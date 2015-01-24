********
Tutorial
********

.. toctree::
   :maxdepth: 2


Install & Usage
===============

Download the `SourcePin source code <https://github.com/TeamHG-Memex/memex-pinterest>`_.

SourcePin is Docker and Fig based. First you need to install docker, see instructions
`here <https://docs.docker.com/installation/#installation>`_. Next install fig ::

    $ sudo pip install fig
    
Now start SourcePin from the repo root directory by typing ::
     
     $ sudo fig up
    
This will take a little while, be patient. Then open up a web browser and go to http://localhost. You should
see SourcePin running.

In order to stop SourcePin go to the root directory of the cloned repo and type ::
    
    $ sudo fig stop
    
To restart SourcePin type ::

    $ sudo fig start
    
An important note: be careful with the sudo fig up command, it will clear your data and give you a clean
instance of SourcePin. Instead, if you want to stop and start without clearing the database, use start/stop.
This is important.

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