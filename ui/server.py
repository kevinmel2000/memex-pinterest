from flask import Flask
from flask import render_template, jsonify, Response
from handlers import request_wants_json
from mongoutils.memex_mongo_utils import MemexMongoUtils 
from handlers import hosts_handler
import json
app = Flask(__name__)

@app.route("/discovery")
def discovery():
    
    return render_template('discovery.html')

#services
@app.route("/")
@app.route("/hosts")
def domain():

    hosts = hosts_handler()

    if request_wants_json():
        return Response(json.dumps(hosts), mimetype = "application/json")

    return render_template('index.html', hosts = hosts)

@app.route("/urls")
@app.route("/urls/<host>")
def urls():
    
    return "dddddddddddddddddddd"

#    return render_template("", urls = urls)

if __name__ == "__main__":

    app.debug = True
    app.run('0.0.0.0')
