"""
Base Flask App for Poo Mailer
"""

from flask import Flask, session, render_template, request
import json

import keys
from ship import ship_to_address
from countries import COUNTRIES
from record import email_shipment_info

app = Flask(__name__)

# Handles both login and displaying form
#
@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        if request.form['password'] == keys.LOGIN_PASSWORD:
            session['logged_in'] = True
        else:
            session['logged_in'] = False
            return render_template('login.html', prompt='Wrong Password')
    if 'logged_in' in session and session['logged_in'] == True:
        return render_template('home.html', countries=COUNTRIES, title='Home')
    else:
        session['logged_in'] = False
        return render_template('login.html')

# Handles ajax of form submission
#
@app.route("/submit", methods=["POST"])
def submit():
    if 'logged_in' not in session:
        status = {'status': 'error', 'message': 'You are not logged in'}
        return json.dumps(status)
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

# Helper function for submit() that processes data into dicts
def build_data_dict(keys, form):
    data_dict = {}
    for key in keys:
        if key in form:
            data_dict[key] = form.get(key)
        else:
            data_dict[key] = ''
    return data_dict

# Start the app
#
if __name__ == "__main__":
    app.debug = keys.DEBUG
    app.secret_key = keys.SECRET_KEY
    app.run(host='0.0.0.0', port=9001)
