"""
Base Flask App
"""

from flask import Flask, render_template, request
import json

from keys import DEBUG
from ship import ship_to_address
from countries import COUNTRIES
from record import email_shipment_info

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('home.html', countries=COUNTRIES, title='Home')

@app.route("/submit", methods=["POST"])
def submit():
    address_dict = {
        'name': request.form['name'],
        'company': request.form['company'],
        'street1': request.form['address_line1'],
        'street2': request.form['address_line2'],
        'city': request.form['city'],
        'state': request.form['region'],
        'zip': request.form['postal_code'],
        'country': request.form['country'],
        'phone': request.form['phone'],
    }
    parcel_info = {
        'length': request.form['length'],
        'width': request.form['width'],
        'height': request.form['height'],
        'weight': request.form['weight']
    }
    options = {
        'dry_ice_weight': request.form['dry_ice'],
        'print_custom_1': request.form['print_custom_1']
    }
    email = request.form['email'];

    status = ship_to_address(address_dict, parcel_info, options=options)
    if status['status'] == 'success':
        email_shipment_info(status, email)
    return json.dumps(status)

if __name__ == "__main__":
    if DEBUG:
        app.debug = True
    app.run(host='0.0.0.0', port=9001)
