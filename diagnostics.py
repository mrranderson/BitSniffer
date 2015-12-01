from blockchain_info import *

def build_tx_edges(blocks, first_tx):
    """ Given a transaction and a list of blocks, find all other transactions in
    those blocks that received coins from the initial transaction.
    """
    # keep track of addresses. These are 2-tuples that represent transactions
    # where the first element is an input and the second element is an output. 
    edges = [first_tx]

    # for every block between the two transactions, if we see any known address
    # as the input to a transaction, we add all of the output addresses to 
    for block in blocks:
        new_edges = []
        for tx in block['tx']:
            input_addrs = get_input_addrs(tx)
            output_addrs = get_output_addrs(tx)
            known_output_addrs = [x[1] for x in edges]

            for input_addr in input_addrs:
                for known_output_addr in known_output_addrs:
                    if input_addr == known_output_addr:
                        tuples = [(input_addr, x) for x in output_addrs]
                        new_edges.extend(tuples)
                        break

       edges.extend(new_addrs)

    return known_addrs


def direct_link_exists(tx_in_hash, tx_out_hash):
    """
    Returns a list of transactions that link the two addresses 

    Note: 
    if there's more than one output in either transaction, we don't have
    enough information to know which addresses belong to the user.
    (This can be changed later. It simplifies our code right now.)
    """
    # fetch the transactions going into and out of the mixing service
    tx_in = get_tx(tx_in_hash)
    tx_out = get_tx(tx_out_hash)
    blocks = get_blocks_between_txs(tx_in, tx_out)

    # the address provided by the mixer
    start_addr =  tx_in['out'][0]['addr']

    # the address the user provides
    end_addr   = tx_out['out'][0]['addr']

    # the first transaction going into the mixer, represented as a 2-tuple of
    # addresses
    first_tx = (tx_in['inputs'][0]['addr'], start_addr)

    edges = build_tx_edges(blocks, first_tx)
    # Now we have 


