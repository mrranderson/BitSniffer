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
    return _retrieve(tx_hash, "TX")

def get_addr(addr): 
    return _retrieve(addr, "ADDR")

def get_block(block_hash): 
    return _retrieve(block_hash, "BLOCK")

def get_block_from_height(block_height):
    blocks = _retrieve(block_height, "BLOCKHEIGHT")
    if len(blocks['blocks'] > 1):
        raise RuntimeError(
            """There is more than one block at height {}. Try waiting a little
            bit for the blockchain to come together.""")
    return blocks['blocks'][0]

