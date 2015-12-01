""" 
Contains helper functions, mostly for manipulating blockchain elements
and performing sub-operations on them.
"""

def is_outgoing_tx(tx, addr):
    """ Returns True if a transaction is outgoing relative
    to an address addr.
    """
    outputs = tx["out"]
    dests = [x["addr"] for x in outputs]
    # addr not in dests of any output, then it must be the source in one of the
    # inputs for it to be associated with this address
    return addr not in dests

def find_tx_by_output_amt(block, interval):
    """ Interval is a tuple of (int, int) in satoshis 
    that gives the range, inclusive, we should return tx's for. """ 

    possible_range = range(interval[0], interval[1]+1)
    possible_txs = []
    for tx in block['tx']:
        for output in tx['out']:
            if output['value'] in possible_range:
                possible_txs.append(tx)
                break
    
    return possible_txs

def get_next_tx_hashes(tx_hash):
    try:
        pklname = tx_hash + '.pkl'
        if pklname in os.listdir('/tmp'):
            with open('/tmp/' + pklname, 'rb+') as f:
                r = pickle.load(f)
        else:
            r = bc.get_transaction_details(tx_hash, api_key=API_KEY)
            #sleep(0.2)
            with open('/tmp/' + pklname, 'wb+') as f:
                pickle.dump(r, f)
        r = r['outputs']
        return [ x["spent_by"] for x in r if "spent_by" in x]
    except: 
        print("Something bad happened when trying to call blockcypher.")
        print(r)
        print(sys.exc_info()[0])
        raise


