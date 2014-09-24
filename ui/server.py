from flask import Flask
from flask import render_template, jsonify, Response
from handlers import request_wants_json
from mongoutils.memex_mongo_utils import MemexMongoUtils 
from handlers import hosts_handler, urls_handler
import json
app = Flask(__name__)

#ui
@app.route("/discovery")
def discovery():
    
    return render_template('discovery.html')

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

    #change this
    return render_template("urls.html", urls = urls, use_cc_data = False)

@app.route("/cc-urls")
@app.route("/cc-urls/<host>")
def cc_urls(host = None):

    urls = urls_handler(host, which_collection = "cc-crawl-data")
    if request_wants_json():
        return Response(json.dumps(urls), mimetype = "application/json")

    #change this
    return render_template("urls.html", urls = urls, use_cc_data = True)

if __name__ == "__main__":

    app.debug = True
    app.run('0.0.0.0')
