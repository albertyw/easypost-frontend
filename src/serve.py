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

def build_data_dict(keys, form):
    data_dict = {}
    for key in keys:
        if key in form:
            data_dict[key] = form.get(key)
        else:
            data_dict[key] = ''
    return data_dict

@app.route("/submit", methods=["POST"])
def submit():
    address_keys = ['name', 'company', 'street1', 'street2', 'city', 'state', 'zip', 'country', 'phone']
    parcel_keys = ['length', 'width', 'height', 'weight']
    option_keys = ['dry_ice_weight', 'print_custom_1']

    address_dict = build_data_dict(address_keys, request.form)
    parcel_dict = build_data_dict(parcel_keys, request.form)
    options_dict = build_data_dict(option_keys, request.form)

    status = ship_to_address(address_dict, parcel_dict, options=options_dict)
    if status['status'] == 'success':
        email_shipment_info(status)
    return json.dumps(status)

if __name__ == "__main__":
    if DEBUG:
        app.debug = True
    app.run(host='0.0.0.0', port=9001)
