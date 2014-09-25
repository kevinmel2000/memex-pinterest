import random
import os
from flask import Flask
from operator import itemgetter
from flask import render_template, jsonify, Response, request
from handlers import request_wants_json
from mongoutils.memex_mongo_utils import MemexMongoUtils 
from handlers import hosts_handler, urls_handler, schedule_spider_handler, get_job_state_handler, schedule_spider_handler, discovery_handler, mark_interest_handler, get_screenshot_relative_path
import json
import hashlib
server_path = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__)

#ui
@app.route("/discovery")
def discovery():
    
    seeds = discovery_handler()
    for seed in seeds:
        seed["url_hash"] = str(hashlib.md5(seed["url"]).hexdigest())
    return render_template('discovery.html', seeds = seeds)

@app.route("/data")
@app.route("/")
def data(page = 1):

    hosts = hosts_handler(page = int(page))

    return render_template('data.html', hosts = hosts, which_collection = "crawl-data", use_cc_data = False)

@app.route("/cc-data")
def cc_data(page = 1):

    hosts = hosts_handler(page = int(page), which_collection = "cc-crawl-data")

    return render_template('data.html', hosts = hosts, use_cc_data = True)

#services
@app.route("/hosts/<page>")
def load_hosts(page = 1):

    hosts = hosts_handler(page = int(page))

    if request_wants_json():
        return Response(json.dumps(hosts), mimetype = "application/json")

    return render_template('hosts.html', hosts = hosts, use_cc_data = False)

@app.route("/cc-hosts/<page>")
def cc_load_hosts(page = 1):

    hosts = hosts_handler(page = int(page), which_collection = "cc-crawl-data")

    if request_wants_json():
        return Response(json.dumps(hosts), mimetype = "application/json")

    return render_template('hosts.html', hosts = hosts, which_collection = "cc-crawl-data", use_cc_data = True)

@app.route("/urls")
@app.route("/urls/<host>")
def urls(host = None):

    urls = urls_handler(host)
    if request_wants_json():
        return Response(json.dumps(urls), mimetype = "application/json")

    #!super hacky
    for url_dic in urls:
        screenshot_path = url_dic["screenshot_path"]
        url_dic["screenshot_path"] = get_screenshot_relative_path(screenshot_path)

    return render_template("urls.html", urls = urls)

@app.route("/cc-urls")
@app.route("/cc-urls/<host>")
def cc_urls(host = None):

    urls = list(urls_handler(host, which_collection = "cc-crawl-data"))
    if request_wants_json():
        return Response(json.dumps(urls), mimetype = "application/json")

    #change this
    return render_template("urls.html", urls = urls, use_cc_data = True)

@app.route("/schedule-spider/")
def schedule_spider():


    url = request.args.get('url')
    schedule_spider_handler(url)
    return Response("OK")

@app.route("/url-job-state/")
def get_spider_update():

    url = request.args.get('url')
    state = get_job_state_handler(url)

    return str(state)

@app.route("/mark-interest/<interest>/")
def mark_interest(interest):

    url = request.args.get('url')

    if interest.strip().lowr() == "false":
        interest = False

    elif interest.strip().lower() == "true":
        interest = True, x["score"]

    else:
        raise Exception("Interest must be either true or false")

    ret = mark_interest_handler(interest, url)
    return Response("OK")

if __name__ == "__main__":
    app.debug = True
    app.run('0.0.0.0', threaded = True)
