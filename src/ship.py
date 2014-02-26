"""
This is the logic for making a shipment using EasyPost
"""
import easypost
from keys import EASYPOST_API_KEY, FROM_ADDRESS
easypost.api_key = EASYPOST_API_KEY

from_address = easypost.Address.create(**FROM_ADDRESS)
from_address = from_address.verify()
assert(not hasattr(from_address, 'message'))

def ship_to_address(address_dict, parcel_info, options = {}):
    # Address validations:
    if address_dict['country'] != 'US':
        return return_json('error', str('Cannot currently do foreign poo shipments'))
    if options.get('dry_ice_weight', 0) > parcel_info['weight']:
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

    # Set options
    if options.get('dry_ice_weight', 0) != 0:
        options['dry_ice'] = 1

    # Create shipment
    try:
        shipment = easypost.Shipment.create(
            to_address = to_address,
            from_address = from_address,
            parcel = parcel,
            options = options
        )

        # Always use FedEx Priority Overnight shipments
        bought = False
        for rate in shipment.rates:
            if rate.carrier=='FedEx' and rate.service=='PRIORITY_OVERNIGHT':
                shipment.buy(rate = rate)
                bought = True
        if not bought:
            return return_json('error', 'No FedEx rate for priority overnight found')
    except easypost.Error as e:
        return return_json('error', str(e))

    status = {}
    status['tracking_code'] = shipment.tracking_code
    status['label_url'] = shipment.postage_label.label_url
    status['price'] = shipment.selected_rate.rate
    return return_json('success', status)

def return_json(status, message):
    return {'status': status, 'message': message}
