"""
Base Flask App
"""

from flask import Flask, render_template, request
app = Flask(__name__)

from keys import DEBUG
from ship import ship_to_address
from countries import COUNTRIES

@app.route("/")
def hello():
    return render_template('home.html', countries=COUNTRIES, title='Home')

@app.route("/submit", methods=["POST"])
def submit():
    address_dict = {
        'name': request.form['name'],
        'street1': request.form['address_line1'],
        'street2': request.form['address_line2'],
        'city': request.form['city'],
        'state': request.form['region'],
        'zip': request.form['postal_code'],
        'country': request.form['country'],
    }
    parcel_info = {
        'length': request.form['length'],
        'width': request.form['width'],
        'height': request.form['height'],
        'weight': request.form['weight']
    }

    status = ship_to_address(address_dict, parcel_info)
    return status

if __name__ == "__main__":
    if DEBUG:
        app.debug = True
    app.run(host='0.0.0.0', port=9001)
