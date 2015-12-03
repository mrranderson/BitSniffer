import blockchain_info

def _build_tx_edges(blocks, first_tx):
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
            input_addrs = blockchain_info.get_input_addrs(tx)
            output_addrs = blockchain_info.get_output_addrs(tx)
            known_output_addrs = [x[1] for x in edges]

            for input_addr in input_addrs:
                for known_output_addr in known_output_addrs:
                    if input_addr == known_output_addr:
                        new_edges.extend(
                            [(input_addr, x) for x in output_addrs] )
                        break

        edges.extend(new_edges)

    print(edges)
    exit()

    return edges 

def _build_tx_edges_dict(blocks, first_tx):
    """ Given a transaction and a list of blocks, find all other transactions in
    those blocks that received coins from the initial transaction.

    Args:
        blocks, list, a list of block dictionaries, as defined by the 
            Blockchain.info API: https://blockchain.info/api/blockchain_api
        first_tx, tuple, a tuple of length 2: the first element is a string
            representing the sending address in the first transaction; the 
            second element is a string representing the receiving address in 
            the transaction

    Returns:
        sub_graph, dictionary, a dict that maps a string (the sending address)
            to a set that contains every address that has received BTC from the
            sending address
    """

    # first we need to look through all of the blocks and build a graph for all
    # of them

    graph = {}
    graph[first_tx[0]] = set()
    graph[first_tx[0]].add(first_tx[1])
    graph[first_tx[1]] = set()

    for block in blocks:
        for tx in block['tx']:
            input_addrs = blockchain_info.get_input_addrs(tx)
            output_addrs = blockchain_info.get_output_addrs(tx)

            for input_addr in input_addrs:
                if input_addr not in graph:
                    graph[input_addr] = set()
                
                for output_addr in output_addrs:
                    if output_addr != input_addr:
                        graph[input_addr].add(output_addr)

    # now we perform a BFS and generate the subgraph of transactions that are
    # connected (somehow) to the input transaction

    sub_graph = {}
    sub_graph[first_tx[0]] = set()
    sub_graph[first_tx[0]].add(first_tx[1])
    sub_graph[first_tx[1]] = set()

    queue = []
    queue.append(first_tx[1])

    while len(queue) > 0:
        adr = queue.pop()

        if adr not in sub_graph:
            sub_graph[adr] = set()

        if adr in graph:
            for adr2 in graph[adr]:
                sub_graph[adr].add(adr2)

                if adr2 not in queue:
                    queue.append(adr2)

    return sub_graph

def _find_path(edges, start_addr, end_addr):
    """ Takes a list of edges created in _build_tx_edges and two addresses.
    Returns None if no path, otherwise a list of addresses. 
    """

    print(edges)

    return None

def direct_link_exists(tx_in_hash, 
                       tx_out_hash, 
                       user_start_addr, 
                       user_end_addr,
                       mixer_input_addr):
    """Returns a list of transactions that link the two addresses.

    Args:
        tx_in_hash, string, transaction id hash of the input transaction to the
            mixer (this is significant to the Blockchain.info API)
        tx_out_hash, string, transaction id has of the output transction to the
            mixer
        user_start_addr, string, the address used to send BTC to the mixer
        user_end_addr, string, the address used to receive BTC from the mixer
        mixer_input_addr, string, the address the mixer uses to receive BTC
    """
    # fetch the transactions going into and out of the mixing service
    # also fetch block objects between the two
    tx_in = blockchain_info.get_tx(tx_in_hash)
    tx_out = blockchain_info.get_tx(tx_out_hash)
    blocks = blockchain_info.get_blocks_between_txs(tx_in, tx_out)

    # the first transaction going into the mixer, represented as a 2-tuple
    first_tx = (user_start_addr, mixer_input_addr)
    edges = _build_tx_edges(blocks, first_tx)
    print(edges)
    print(len(edges))

    path = _find_path(edges, user_start_addr, user_end_addr)
    if path:
        return True
    else:
        return False

def get_anonymity_set(tx_in_hash, tx_out_hash, user_start_addr, user_end_addr,
        mixer_input_addr, start_time, end_time, flat_fee, percent_fee_lower,
        percent_fee_upper): 
    """
    Returns a set of tx hashes that fall within the range. start_time and
    end_time in hours, flat_fee in satoshis.
    """
    # construct satoshi interval, then 
    # call find_tx_by_output_amt inside a loop over blocks
    # in the time interval
    pass


    #CHANGEME
def find_tx_by_output_amt(block, interval):
    """ Interval is a tuple of (int, int) (satoshis) 
    that gives the range, inclusive, we should return tx's for. """ 

    possible_range = range(interval[0], interval[1]+1)
    possible_txs = []
    for tx in block['tx']:
        for output in tx['out']:
            if output['value'] in possible_range:
                possible_txs.append(tx)
                break
    
    return possible_txs


