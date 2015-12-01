"""
This contains methods to retrieve and manipulate blockchain information using
blockchain.info's API. Methods are cached as necessary in _PKL_DIR.
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

def get_block(block_hash): 
    """ Returns block object """
    return _retrieve(block_hash, "BLOCK")

def get_block_from_height(block_height):
    """ Returns block object from height. Assume there's only one. """
    blocks = _retrieve(block_height, "BLOCKHEIGHT")
    if len(blocks['blocks'] > 1):
        raise RuntimeError(
            """There is more than one block at height {}. Try waiting a little
            bit for the blockchain to come together.""")
    return blocks['blocks'][0]

def get_blocks_between_txs(tx_in, tx_out):
    """ Returns a list of all blocks between the two txs, inclusive """
    start_height =  tx_in['out'][0]['block_height']
    end_height   = tx_out['out'][0]['block_height']
    blocks = [get_block_from_height(h) for h in range(start_height, end_height+1)]

def get_input_addrs(tx):
    """ Takes tx object and returns the input addresses associated. """
    return [x['prev_out']['addr'] for x in tx['inputs']]

def get_output_addrs(tx):
    """ Takes tx object and returns the output addresses associated. """
    return [x['addr'] for x in tx['out']]

