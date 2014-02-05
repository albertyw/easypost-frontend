"""
This is the logic for setting up shipping from easypost
"""

import easypost
from keys import *
easypost.api_key = EASYPOST_API_KEY

from_address = easypost.Address.create(
        company = 'Alm Laboratory',
        street1 = '500 Technology Square',
        city = 'Cambridge',
        state = 'MA',
        zip = '02139',
        country = 'US'
    )
from_address = from_address.verify()


def ship_to_address(address_dict):
    # Address validations:
    assert(address_dict['country'] == 'US')

    # Create To Address
    to_address = easypost.Address.create(**address_dict)
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

