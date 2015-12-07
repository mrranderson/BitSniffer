"""
This contains methods to retrieve and manipulate blockchain information using
blockchain.info's API. JSONs returned by the API are cached as necessary in 
_PKL_DIR.
"""
import requests as reqs
import pickle
import os

_join = os.path.join
_ls = os.listdir

# Cache directory
_PKL_DIR = './.pickles'

try:
    os.mkdir(_PKL_DIR)
    print("Initialized cache at {}".format(_PKL_DIR))
except OSError:
    print("Using cache at {}".format(_PKL_DIR))

# Base URLs for API
_BASEBLOCK = 'https://blockchain.info/rawblock/{}'
_BASETX = 'https://blockchain.info/rawtx/{}'
_BASEADDR = 'https://blockchain.info/rawaddr/{}'
_BASEBLOCKHEIGHT = 'https://blockchain.info/block-height/{}?format=json'

# For use in `_retrieve`
TYPE_MAP = {
    "TX"          : _BASETX,
    "ADDR"        : _BASEADDR,
    "BLOCK"       : _BASEBLOCK,
    "BLOCKHEIGHT" : _BASEBLOCKHEIGHT,
}

def _retrieve(name, type):
    """ Checks cache for a pickle. 
    If pickle is not in cache, _retrieves the block/tx/addr, caches it,
    and returns. 
    """
    pklname = name + '.pkl'
    if pklname in _ls(_PKL_DIR):
        with open(_join(_PKL_DIR, pklname), 'rb') as f:
            return pickle.load(f)

    obj = reqs.get(TYPE_MAP[type].format(name)).json()
    with open(_join(_PKL_DIR, pklname), 'wb') as f:
        pickle.dump(obj, f)
    return obj

def get_tx(tx_hash): 
    """ Returns tx object """
    return _retrieve(tx_hash, "TX")

def get_addr(addr): 
    """ Returns addr object """
    return _retrieve(addr, "ADDR")

def get_all_sent_txs_for_addr(addr):
    """Given an address, this returns a list of tx objects (as defined by the
    blockchain.info API) that represent outgoing transactions from the address.
    """

    addr_obj = get_addr(addr)
    sent_txs = []

    for tx in addr_obj["txs"]:
        if addr in get_input_addrs(tx):
            sent_txs.append(tx)

    return sent_txs

def get_all_received_txs_for_addr(addr):
    """Given an address, this returns a list of tx objects (as defined by the
    blockchain.info API) that represent incoming transactions from the address.
    """

    addr_obj = get_addr(addr)
    received_txs = []

    for tx in addr_obj["txs"]:
        if addr in get_output_addrs(tx):
            received_txs.append(tx)

    return received_txs

def get_block(block_hash): 
    """ Returns block object """
    return _retrieve(block_hash, "BLOCK")

def get_block_from_height(block_height):
    """ Returns block object from height. Assume there's only one. """
    blocks = _retrieve(str(block_height), "BLOCKHEIGHT")
    if len(blocks['blocks']) > 1:
        raise RuntimeError(
            """There is more than one block at height {}. Try waiting a little
            bit for the blockchain to come together.""")
    return blocks['blocks'][0]

def get_blocks_between_txs(tx_in, tx_out):
    """ Returns a list of all blocks between the two txs, inclusive """
    start_height =  tx_in['block_height']
    end_height   = tx_out['block_height']
    return [get_block_from_height(h) for h in range(start_height, end_height+1)]

def get_blocks_in_time_range(tx_in, start_time, end_time):
    """
    Return a list of all blocks starting start_time after tx_in, ending end_time after 
    tx_in, where start_time and end_time are in hours after the initial transaction

    Args: 
        tx_in, object, a representation of the JSON that blockchain.info's API
            provides for transactions
        start_time, int, starting offset (in hours) from tx_in's block 
        end_time, int, ending offset (in hours) from tx_in's block

    Returns:
        blocks, list, a list of block objects (obtained from blockchain.info's
            API) that were discovered between the given time range.
    """
    start_block = get_block_from_height(tx_in['block_height'])

    start_height = tx_in['block_height']
    height = int(start_block['height'])
    blocks = []

    current_block = start_block 

    # Starting at the block the input transaction is in, loop through blocks until 
    # you reach the longest time the mixer said it would take to return your coins
    # If the block is between start and end times, add it to the anonymity set
    while current_block['time'] < start_block['time']+3600*end_time:
        if current_block['time'] > start_block['time']+3600*start_time:
            blocks += [current_block]
        height += 1
        current_block = get_block_from_height(height)

    return blocks

def find_tx_by_output_amt(block, interval):
    """ Interval is a tuple of (int, int) (satoshis) 
    that gives the range, inclusive, we should return tx's for. 
    
    Returns an obj of {tx_hash, addr} so we can identify which address in each
    transaction matched later on.
    """ 

    possible_outputs = []
    for tx in block['tx']:
        fee = 0 #get_fee(tx)
        total_output = sum([output['value'] for output in tx['out']])
        for output in tx['out']:
            try:
                proportion = output['value']/total_output
            except ZeroDivisionError:
                proportion = 0
            interval_with_fee = range(interval[0] - int(fee * proportion),
                    interval[1] - int(fee * proportion) + 1)
            if output['value'] in interval_with_fee:
                possible_outputs.append({
                    "tx_hash": tx['hash'], 
                    "addr"   : output['addr']
                })
                break
    
    return possible_outputs

def get_fee(tx):
    """ Takes tx object and returns the transaction fee in satoshis """
    outputs = [output['value'] for output in tx['out']]
    try:
        inputs = [input['prev_out']['value'] for input in tx['inputs']]
    except KeyError:
        # This happens when there's a coinbase transaction
        inputs = []
    return sum(inputs) - sum(outputs)

def get_input_addrs(tx):
    """ Takes tx object and returns the input addresses associated. """
    try:
        return [x['prev_out']['addr'] for x in tx['inputs']]
    except KeyError:
        # This happens when there's a coinbase transaction
        return []

def get_output_addrs(tx):
    """ Takes tx object and returns the output addresses associated. """
    addrs = []
    for x in tx['out']:
        # Sometimes there's no output address for a tx?? see:
        # https://blockchain.info/tx/02f96fe50b6d65c2f784b1e5260915877415330404bc17c66f74e2b5bd06ea14
        try:
            addrs.append(x['addr'])
        except KeyError:
            continue
    return addrs

