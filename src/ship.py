"""
This is the logic for setting up shipping from easypost
"""

import easypost
from keys import *
easypost.api_key = EASYPOST_API_KEY

from_address = easypost.Address.create(
        company = 'Alm Laboratory',
        street1 = '500 Technology Square 3rd Floor',
        city = 'Cambridge',
        state = 'MA',
        zip = '02139',
        country = 'US'
    )
from_address = from_address.verify()
assert(not hasattr(from_address, 'message'))

def ship_to_address(address_dict, parcel_info):
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
        parcel = easypost.Parcel.create(**parcel_info)
    except easypost.Error as e:
        return str(e)

    # create shipment
    shipment = easypost.Shipment.create(
        to_address = to_address,
        from_address = from_address,
        parcel = parcel
    )

    # buy postage label with one of the rate objects
    shipment.buy(rate = shipment.lowest_rate())

    status = {}
    status['tracking_code'] = shipment.tracking_code
    status['label_url'] = shipment.postage_label.label_url
    return str(status)

