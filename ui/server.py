from flask import Flask
from flask import render_template, jsonify, Response
from handlers import request_wants_json
from mongoutils.memex_mongo_utils import MemexMongoUtils 
from handlers import hosts_handler, urls_handler
import json
app = Flask(__name__)

#app
@app.route("/discovery")
def discovery():
    
    return render_template('discovery.html')

@app.route("/")
def index(page = 1):

    hosts = hosts_handler(page = int(page))

    return render_template('index.html', hosts = hosts)

#services
@app.route("/hosts/<page>")
def load_hosts(page = 1):

    hosts = hosts_handler(page = int(page))

    if request_wants_json():
        return Response(json.dumps(hosts), mimetype = "application/json")

    return render_template('hosts.html', hosts = hosts)

@app.route("/urls")
@app.route("/urls/<host>")
def urls(host = None):

    urls = urls_handler(host)
    if request_wants_json():
        return Response(json.dumps(urls), mimetype = "application/json")

    #change this
    return render_template("urls.html", urls = urls)

#    return render_template("", urls = urls)

if __name__ == "__main__":

    app.debug = True
    app.run('0.0.0.0')
