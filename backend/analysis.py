import os

if 'backend' in os.listdir('.'):
    from backend import blockchain_info as bi
else:
    import blockchain_info as bi

class LinkabilityTest:
    def __init__(self):
        self.verbose = False

    def test(self, addr1, addr2, blocks):
        """
        """

        return -1

class TotalAmountSentReceivedTest(LinkabilityTest):
    """This compares the total amount sent and received between two addresses.
    If two addresses have similar amounts sent and received, we consider those
    addresses as being linked.
    """

    def test(self, addr1, addr2, blocks):
        """We assume addr1 sends BTC to addr2. We return a value which is 1 if
        the amount sent is equal to the amount received. As these amounts become
        more different, the value we return approaches 0.

        The range of values we return is 0 -> 1, inclusive.
        """

        addr1_total_sent = bi.get_addr(addr1)["total_sent"]
        addr2_total_received = bi.get_addr(addr2)["total_received"]

        return 1.0 - abs(addr1_total_sent - addr2_total_received) / \
            float(max(addr1_total_sent, addr2_total_received))

class AverageAmountSentReceivedTest(LinkabilityTest):
    """This compares the total amount sent and received between two addresses.
    If two addresses have similar amounts sent and received, we consider those
    addresses as being linked.
    """

    def test(self, addr1, addr2, blocks):
        """We assume addr1 sends BTC to addr2. We return a value which is 1 if
        the amount sent is equal to the amount received. As these amounts become
        more different, the value we return approaches 0.

        The range of values we return is 0 -> 1, inclusive.
        """

        num_addr1_txs = len(bi.get_all_sent_txs_for_addr(addr1))
        num_addr2_txs = len(bi.get_all_received_txs_for_addr(addr2))

        addr1_average_sent = float(bi.get_addr(addr1)["total_sent"])/num_addr1_txs
        addr2_average_received = float(bi.get_addr(addr2)["total_received"])/num_addr2_txs

        return 1.0 - abs(addr1_average_sent - addr2_average_received) / \
            float(max(addr1_average_sent, addr2_average_received))

class AverageNumInputsOutputsTest(LinkabilityTest):
    """
    """

    def test(self, addr1, addr2, blocks):
        """
        """

        addr1_txs = bi.get_all_sent_txs_for_addr(addr1)
        sum_of_all_outputs_per_tx = 0

        for tx in addr1_txs:
            sum_of_all_outputs_per_tx += len(tx['out'])

        ave_num_outputs = sum_of_all_outputs_per_tx / float(len(addr1_txs))

        addr2_txs = bi.get_all_received_txs_for_addr(addr2)
        sum_of_all_inputs_per_tx = 0

        for tx in addr2_txs:
            sum_of_all_inputs_per_tx += len(tx['inputs'])

        ave_num_inputs = sum_of_all_inputs_per_tx / float(len(addr2_txs))

        return 1.0 - abs(ave_num_inputs - ave_num_outputs) / \
            float(max(ave_num_inputs, ave_num_outputs))

class IndividualAmountSentTest(LinkabilityTest):
    """This compares the transactions from two addresses. 
    """

    def test(self, addr1, addr2, blocks):
        """
        """

        print("IndividualAmountSentTest: test()")

        return -1

class DirectLinkExistsTest(LinkabilityTest):
    """
    """

    def test(self, addr1, addr2, blocks):
        """
        """

        print("DirectLinkTest: test()")

        return -1

class TransactionFrequencyTest(LinkabilityTest):
    """
    """

    def test(self, addr1, addr2, blocks):
        """This test compares the 
        """

        addr1_txs = bi.get_all_sent_txs_for_addr(addr1)
        num_addr1_txs = len(addr1_txs)

        youngest_tx = addr1_txs[0]
        oldest_tx = addr1_txs[0]

        for tx in addr1_txs:
            if tx['block_height'] < youngest_tx['block_height']:
                youngest_tx = tx
            elif tx['block_height'] > oldest_tx['block_height']:
                oldest_tx = tx

        addr1_frequency = float(num_addr1_txs)/(oldest_tx['block_height'] - youngest_tx['block_height'] + 1)
        
        addr2_txs = bi.get_all_received_txs_for_addr(addr2)
        num_addr2_txs = len(addr2_txs)

        youngest_tx = addr2_txs[0]
        oldest_tx = addr2_txs[0]

        for tx in addr2_txs:
            if tx['block_height'] < youngest_tx['block_height']:
                youngest_tx = tx
            elif tx['block_height'] > oldest_tx['block_height']:
                oldest_tx = tx

        addr2_frequency = float(num_addr2_txs)/(oldest_tx['block_height'] - youngest_tx['block_height'] + 1)

        return 1 - abs(addr1_frequency - addr2_frequency) / \
            max(addr1_frequency, addr2_frequency)

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
            input_addrs = bi.get_input_addrs(tx)
            output_addrs = bi.get_output_addrs(tx)
            known_output_addrs = [x[1] for x in edges]

            for input_addr in input_addrs:
                for known_output_addr in known_output_addrs:
                    if input_addr == known_output_addr:
                        new_edges.extend(
                            [(input_addr, x) for x in output_addrs] )
                        break

        edges.extend(new_edges)

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
            input_addrs = bi.get_input_addrs(tx)
            output_addrs = bi.get_output_addrs(tx)

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
        addr = queue.pop()

        if addr not in sub_graph:
            sub_graph[addr] = set()

        if addr in graph:
            for addr2 in graph[addr]:
                sub_graph[addr].add(addr2)

                if addr2 not in queue:
                    queue.append(addr2)

    return sub_graph

def _find_path(graph, start_addr, end_addr):
    """Determines if there is a path from start_addr to end_addr (note that
    edges in the graph are unidirectional).

    Args:
        graph, dict, a dict that maps a string (the sending address) to a set
            that contains every address that has received BTC from the sending
            address
        start_addr, string, the starting (sending) address for the path
        end_addr, string, the ending (receiving) address for the path

    Returns:
        None, if no path, otherwise a list of addresses representing the path
    """

    if type(graph) is not dict:
        raise TypeError("graph should be a dictionary")

    if start_addr not in graph:
        return None

    # now, we perform a DFS...

    parent_mapping = {} # maps a child addr to its parent
    stack = []
    stack.insert(0, start_addr) # the equivalent of push()

    while len(stack) > 0:
        addr = stack.pop()

        # if the current address being considered is the end address, we need
        # traverse back through the graph to start_addr and keep track of the 
        # path along the way

        if addr == end_addr:
            path = []
            path.append(addr)
            parent = parent_mapping[addr]

            while parent != start_addr:
                path.append(parent)
                parent = parent_mapping[parent]

            path.append(parent)

            return path

        for child_addr in graph[addr]:
            stack.insert(0, child_addr)
            parent_mapping[child_addr] = addr

    return None

def get_path(tx_in_hash, 
             tx_out_hash, 
             user_start_addr, 
             user_end_addr,
             mixer_input_addr,
             verbose=False):
    """Returns a list of transactions that link the two addresses.

    Args:
        tx_in_hash, string, transaction id hash of the input transaction to the
            mixer (this is significant to the Blockchain.info API)
        tx_out_hash, string, transaction id has of the output transction to the
            mixer
        user_start_addr, string, the address used to send BTC to the mixer
        user_end_addr, string, the address used to receive BTC from the mixer
        mixer_input_addr, string, the address the mixer uses to receive BTC
        verbose, boolean, flag to enable/disable status printing
    """

    if verbose:
        print("Collecting transactions and blocks...")

    # fetch the transactions going into and out of the mixing service
    # also fetch block objects between the two
    tx_in = bi.get_tx(tx_in_hash)
    tx_out = bi.get_tx(tx_out_hash)
    blocks = bi.get_blocks_between_txs(tx_in, tx_out)

    if verbose:
        print("Building transaction graph...\n")

    # the first transaction going into the mixer, represented as a 2-tuple
    first_tx = (user_start_addr, mixer_input_addr)
    graph = _build_tx_edges_dict(blocks, first_tx)
    
    if verbose:
        print("Graph: (num sending addresses = %d)\n" % (len(graph)))

        for addr in graph:
            print("%s \n--> %s" % (addr, graph[addr]))

        print("\nAttempting to find a path...\n")

    path = _find_path(graph, user_start_addr, user_end_addr)

    if verbose and path:
        print("Found a path!\n")
        print(path)
        print("\n")

    return path


def get_anonymity_set(tx_in_hash, 
                      tx_value, 
                      start_time, 
                      end_time, 
                      flat_fee, 
                      percent_fee_lower,
                      percent_fee_upper, 
                      verbose=False): 
    """This calculates the anonymity set for a transaction through a mixer.

    The anonymity set is a set of transactions which could be mistaken for the
    actual output transaction from the mixer.

    Args:
        tx_in_hash, string, hash of input transaction to the mixer
        tx_value, int, amount of BTC sent to the mixer, in Satoshi
        start_time, int, number of hours after the transaction to the mixer was 
            submitted (this is the lower time-bound for the blocks we need to
            search over)
        end_time, int, number of hours after the transaction to the mixer was 
            submitted (this is the upper time-bound for the blocks we need to
            search over)
        flat_fee, int, flat fee for the mixer, in Satoshi
        percent_fee_lower, float, lower bound for percentage fee to the mixer
        percent_fee_upper, float, upper bound for percentage fee to the mixer

    Returns:
        anonymity_set, list, a list of transactions (as defined by the 
            transaction JSON object from the blockchain.info API) that 
            represents the anonymity set
    """
    anonymity_set = []

    tx_in = bi.get_tx(tx_in_hash)
    ff = float(flat_fee)
    pfl = float(percent_fee_lower)
    pfu = float(percent_fee_upper)
    tx_value = float(tx_value)
    start_time = float(start_time)
    end_time = float(end_time)

    interval = (int(tx_value - (ff + tx_value * pfu)),
                int(tx_value - (ff + tx_value * pfl)))
    blocks = bi.get_blocks_in_time_range(tx_in, start_time, end_time)  

    print(list(map(lambda x: x['height'], blocks)))

    for i, block in enumerate(blocks):
        new_txs = bi.find_tx_by_output_amt(block, interval)
        for x in new_txs:
            x['offset'] = i+1
        anonymity_set += new_txs

    if verbose:
        for x in anonymity_set:
            print(x)

    return anonymity_set

def test_linkability(addr1, addr2, verbose=False):
    """
    """

    tests = [
        TotalAmountSentReceivedTest(),
        AverageAmountSentReceivedTest(),
        # IndividualAmountSentTest(),
        # DirectLinkExistsTest(),
        TransactionFrequencyTest(),
        AverageNumInputsOutputsTest(),
    ]

    # blocks_to_search_over = bi.get_blocks_in_addr_range(addr1, addr2, 
    #     verbose=verbose)

    blocks_to_search_over = bi.get_blocks_for_two_addresses(addr1, addr2)
    # print(type(blocks_to_search_over))

    # print("num blocks in list: %d" % (len(blocks_to_search_over), ))

    for test in tests:
        print("%s: result = %f" % (test.__class__.__name__, 
            test.test(addr1, addr2, blocks_to_search_over)))

if __name__ == "__main__":
    test_linkability("1MDjCqjwnKmMWPxawpgN1UuDfbMUUgqnWw",
                     "1Luke788hdrUcMqdb2sUdtuzcYqozXgh4L", 
                     # "1MDjCqjwnKmMWPxawpgN1UuDfbMUUgqnWw",
                     verbose=True)

    # test_linkability("1FEFqzSuK8S6gdmDea6yzmxq2BRJ1mbvz4",
                     # "18heVLNxGLAQ1MG2wxD4UytfvFXmyxWhWs")


    # direct_link_exists(       
    # print(len(get_anonymity_set(
    #     '490898199a566dcb32a4a9cf45cc7d3cb5f1372e1703c90ad7845acf400f17a5',
    #     'cb9e8ec8ad02d0edd7b7d9abb85b2312304ffda263493e5ee96e83bc2e78ce17',
    #     '1B1tDpsuUBKu25Ktqp8ohziw7qN43FjEQm',
    #     '1MV8oVUWVSLTbWDh8p2hof6J7hfnEm4UXM',
    #     '1Luke788hdrUcMqdb2sUdtuzcYqozXgh4L',
    #     0,
    #     5,
    #     0,
    #     .05,
    #     .06,
    #     verbose=True)))
