from keys import *
import easypost
easypost.api_key = EASYPOST_API_KEY

from flask import Flask, render_template, request
app = Flask(__name__)

from_address = easypost.Address.create(
        company = 'Alm Laboratory',
        street1 = '77 Massachusetts Ave',
        city = 'Cambridge',
        state = 'MA',
        zip = '02139',
        country = 'US'
    )
from_address = from_address.verify()

@app.route("/")
def hello():
    return render_template('home.html', title='Home')

@app.route("/submit", methods=["POST"])
def submit():
    # Create From Address
    from_address

    # Create To Address
    to_address = easypost.Address.create(
        name = request.form['name'],
        street1 = request.form['address_line1'],
        street2 = request.form['address_line2'],
        city = request.form['city'],
        state = request.form['region'],
        zip = request.form['postal_code'],
        country = request.form['country']
    )
    try:
        to_address = to_address.verify()
    except easypost.Error as e:
        return str(e)
    if hasattr(to_address, 'message'):
        return to_address['message']

    # create parcel
    try:
        parcel = easypost.Parcel.create(
            predefined_package = "InvalidPackageName",
            weight = 21.2
        )
    except easypost.Error as e:
        print e.message
        if e.param != None:
            print 'Specifically an invalid param: ' + e.param

    try:
        parcel = easypost.Parcel.create(
            length = 10.2,
            width = 7.8,
            height = 4.3,
            weight = 21.2
        )
    except easypost.Error as e:
        raise e

    # create shipment
    shipment = easypost.Shipment.create(
        to_address = to_address,
        from_address = verified_from_address,
        parcel = parcel
    )

    # buy postage label with one of the rate objects
    shipment.buy(rate = shipment.rates[0])
    # alternatively: shipment.buy(rate = shipment.lowest_rate())

    print shipment.tracking_code
    print shipment.postage_label.label_url


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=9001)