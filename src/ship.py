"""
This is the logic for setting up shipping from easypost
"""
import easypost
from keys import EASYPOST_API_KEY
easypost.api_key = EASYPOST_API_KEY

from_address = easypost.Address.create(
        company = 'Alm Laboratory',
        street1 = '500 Technology Square 3rd Floor',
        city = 'Cambridge',
        state = 'MA',
        zip = '02139',
        country = 'US',
        phone = '6175759658'
    )
from_address = from_address.verify()
assert(not hasattr(from_address, 'message'))

def ship_to_address(address_dict, parcel_info, dry_ice=0):
    # Address validations:
    if address_dict['country'] != 'US':
        return return_json('error', str('Cannot currently do foreign poo shipments'))
    if dry_ice > parcel_info['weight']:
        return return_json('error', str('Dry ice weight is more than package weight'))


    # Create To Address
    to_address = easypost.Address.create(**address_dict)
    try:
        to_address = to_address.verify()
    except easypost.Error as e:
        return return_json('error', str(e))
    if hasattr(to_address, 'message'):
        return return_json('error', to_address['message'])

    # create parcel
    try:
        parcel = easypost.Parcel.create(**parcel_info)
    except easypost.Error as e:
        return return_json('error', str(e))

    try:
        # create shipment
        options = {}
        if dry_ice != 0:
            options['dry_ice'] = '1'
            options['dry_ice_weight'] = dry_ice
        shipment = easypost.Shipment.create(
            to_address = to_address,
            from_address = from_address,
            parcel = parcel,
            options = options
        )

        # buy postage label with one of the rate objects
        shipment.buy(rate = shipment.lowest_rate())
    except easypost.Error as e:
        return return_json('error', str(e))

    status = {}
    status['tracking_code'] = shipment.tracking_code
    status['label_url'] = shipment.postage_label.label_url
    return return_json('success', status)

def return_json(status, message):
    return {'status': status, 'message': message}
