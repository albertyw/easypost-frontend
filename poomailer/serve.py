from keys import *
import easypost
easypost.api_key = EASYPOST_API_KEY

from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('home.html', title='Home')

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form['name']

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=9001)