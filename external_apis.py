import blockcypher
import os
import pickle
import requests
import time

def get_total_received(sending_address, receiving_address):
    """Given 2 addresses, returns how much BTC was received by the 
    receiving_address from the sending_address.
    """

    r, raw_transactions = pickle.load(
        open("pickles/" + receiving_address + ".pickle", 'rb'))

    total = 0

    for tx in r['txrefs']:
        h = tx['tx_hash']
        transaction = raw_transactions[h]
        move_on = False

        for input in transaction['inputs']:
            if sending_address in input['addresses']:
                for output in transaction['outputs']:
                    if receiving_address in output['addresses']:
                        total += output['value']
                        move_on = True

            if move_on:
                break;

    return total

def get_receivers_cached(sending_address):
    """Same as get_receivers(), but using cached values
    """

    r, raw_transactions = pickle.load(
        open("pickles/" + sending_address + ".pickle", 'rb'))

    receiving_addresses = set()
    index = 0

    for tx in r['txrefs']: # loop through all transactions
        hash = tx['tx_hash']
        transaction = raw_transactions[hash]
        # was this address an input
        sender = False

        for input in transaction['inputs']:
            if sending_address in input['addresses']:
                sender = True
                break
        
        if sender:
            for output in transaction['outputs']:
                for adr in output['addresses']:
                    receiving_addresses.add((adr, output['value']))

        index += 1

    return receiving_addresses

def get_receivers(sending_address):
    """Based on code from: http://bitcoin-class.org/ps/ps3/

    This uses the BlockCypher API. Since I was lazy and didn't register for an
    API key, I wait 0.2 seconds before each request to honor BlockCypher's API
    limits (5 requests/sec).
    """

    if os.path.isfile("pickles/" + sending_address + ".pickle"):
        print("Using cached version...")
        return get_receivers_cached(sending_address)

    receiving_addresses = set()
    time.sleep(0.2)
    r = blockcypher.get_address_details(sending_address)
    raw_transactions = {}

    for tx in r['txrefs']: # loop through all transactions
        hash = tx['tx_hash']
        time.sleep(0.2)
        transaction = blockcypher.get_transaction_details(hash)
        raw_transactions[hash] = transaction
        # was this address an input
        sender = False

        for input in transaction['inputs']:
            if sending_address in input['addresses']:
                sender = True
                break
        
        if sender:
            for output in transaction['outputs']:
                for adr in output['addresses']:
                    receiving_addresses.add((adr, output['value']))

    pickle.dump((r, raw_transactions), 
        open("pickles/" + sending_address + ".pickle", "wb"))

    return receiving_addresses

def get_aka(adr):
    """This calls the Wallet Explorer API to try to attribute adr to a name.

    (based off of code from http://bitcoin-class.org/ps/ps3/)
    """

    if os.path.isfile("pickles/" + adr + "_aka.pickle"):
        r = pickle.load(open("pickles/" + adr + "_aka.pickle", 'rb'))
        if 'label' in r:
            return r['label']
        else:
            return adr

    try:
        r = requests.get(
            'https://www.walletexplorer.com/api/1/address-lookup?address=' \
                 + adr + '&caller=virginia.edu').json()
        pickle.dump(r, open("pickles/" + adr + "_aka.pickle", "wb"))
        return r['label']

    except:
        # print("Found no alternate identity on Wallet Explorer API for " + \
        #    "address: %s" % (adr))
        return adr