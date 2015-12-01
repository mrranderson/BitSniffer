from api_requests import get_tx, get_block, get_addr, get_block_from_height

def direct_link_exists(tx_in_hash, tx_out_hash):
    """
    Returns a list of transactions that link the two addresses 
    """
    # fetch the transactions going into and out of the mixing service
    tx_in = get_tx(tx_in_hash)
    tx_out = get_tx(tx_out_hash)

    # if there's more than one output in either transaction, we don't have
    # enough information to know which addresses belong to the user.
    # (This can be changed later.)
    if len(tx_in['out']) > 1 or len(tx_in['out']) > 1:
        raise NotImplementedError(
            """tx_in and tx_out must have one output address
            and one input address, respectively""")
    
    start_height =  tx_in['out'][0]['block_height']
    end_height   = tx_out['out'][0]['block_height']

    # fetch block objects
    blocks = [get_block_from_height(h) for h in range(start_height, end_height+1)]

    start_addr =  tx_in['out'][0]['addr']
    end_addr   = tx_out['out'][0]['addr']


    

