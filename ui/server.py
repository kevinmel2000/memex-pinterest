from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route("/")
def index():

    sites = [{"url" : "http://www.hyperiongray.com/"}, {"url" : "http://eeeee.com/<script>alert(33)</script>"}]

    return render_template('index.html', sites = sites)

@app.route("/discovery")
def discovery():
    
    return render_template('discovery.html')

if __name__ == "__main__":

    app.debug = True
    app.run('0.0.0.0')
