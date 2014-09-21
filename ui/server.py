from flask import Flask
from flask import render_template, jsonify, Response
from handlers import request_wants_json
from mongoutils.memex_mongo_utils import MemexMongoUtils 
import json
app = Flask(__name__)

#webapp
@app.route("/")
def index():

    #!should be replaced by results of query to mongo
    domains = [{"domain" : "www.hyperiongray.com/"}, {"domain" : "eeeee.com"}]

    return render_template('index.html', domains = domains)

@app.route("/discovery")
def discovery():
    
    return render_template('discovery.html')

#services
@app.route("/domains")
def domain():

    mmu = MemexMongoUtils()
    hosts = mmu.list_hosts()

    if request_wants_json():
        return Response(json.dumps(hosts), mimetype = "application/json")

    return render_template('index.html', hosts = hosts)

@app.route("/urls/<domain>")
def urls():
    
    return render_template("", urls = urls)

if __name__ == "__main__":

    app.debug = True
    app.run('0.0.0.0')
