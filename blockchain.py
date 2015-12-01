import blockcypher as bc
import pickle
import os
import requests
import sys
from time import sleep

import networkx as nx
import matplotlib.pylab
import matplotlib.pyplot as plt


API_KEY='7a26d6bb9d6e87b25b5d8cfc177cf0e5'
RAWBLOCK = 'https://blockchain.info/rawblock/'
RAWTX = 'https://blockchain.info/rawtx/'
RAWADDR = 'https://blockchain.info/rawaddr/'
PICKLE_DIR = '/tmp/'

def address_display(adr):
    try:
        r = requests.get(
                'https://www.walletexplorer.com/api/1/address-lookup?address=' 
		 + adr + '&caller=virginia.edu').json()
        return adr + " (" + r['label'] + ")"
    except:
        return adr

def get_tx(tx_hash):
    pklname = tx_hash + '.pkl'
    if pklname in os.listdir('/tmp'):
        with open('/tmp/' + pklname, 'rb+') as f:
            tx = pickle.load(f)
    else:
        tx = requests.get(RAWTX + tx_hash).json()
        with open('/tmp/' + pklname, 'wb+') as f:
            pickle.dump(tx, f)
    return tx 

def get_block(block_hash):
    pklname = block_hash + '.pkl'
    if pklname in os.listdir('/tmp'):
        with open('/tmp/' + pklname, 'rb+') as f:
            block = pickle.load(f)
    else:
        block = requests.get(RAWBLOCK + block_hash).json()
        with open('/tmp/' + pklname, 'wb+') as f:
            pickle.dump(block, f)
    return block

def get_addr(addr):
    pklname = addr + '.pkl'
    if pklname in os.listdir('/tmp'):
        with open('/tmp/' + pklname, 'rb+') as f:
            addr = pickle.load(f)
    else:
        addr = requests.get(RAWADDR + addr).json()
        with open('/tmp/' + pklname, 'wb+') as f:
            pickle.dump(addr, f)

    return addr 

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

def is_outgoing_tx(tx, addr):
    outputs = tx["out"]
    dests = [x["addr"] for x in outputs]
    # addr not in dests of any output, then it must be the source in one of the
    # inputs for it to be associated with this address
    return addr not in dests

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

def problem5():
    hash_379818 = '00000000000000000fa81e732d2f09af595fbe73348bfb152a48b5b648ca4934'
    block = get_block(hash_379818)

    results = find_tx_by_output_amt(block, (1463862, 1465385))
    print("Found {} possible matches: ".format(len(results)))
    for result in results:
        print(result['hash'])
        print(result['inputs'])
        print(result['out'])

def mod_problem5():
    i = 379850
    hsh = '00000000000000000d09a5efe71f60578ef35316bcd8245a1695f12b4abb9481'
    while True:
        if i == 379817:
            break
        block = get_block(hsh)

        results = find_tx_by_output_amt(block, (1463862, 1465385))
        print("Found {} possible matches in block {}: "
                .format(len(results), i))
        for result in results:
            print(result['hash'])

        hsh = block["prev_block"]
        i -= 1

addr_map = {}
visited_addrs = []
known_txs = []
DEPTH_LIMIT = 2
received = {}
def build_graph(addr, depth=0):
    """
    DFS algorithm that builds a directed graph, represented as a dictionary.
    The directed graph maps from address to list of address, making it
    easy to work with.
    """
    global addr_map, known_txs, visited_addrs

    if depth > DEPTH_LIMIT or addr in visited_addrs:
        return
    visited_addrs.append(addr)

    # initialize dict entry
    if addr not in addr_map:
        addr_map[addr] = list()
        received[addr] = 0

    # find all transactions associated with the address
    txs = get_addr(addr)["txs"]

    # for the first level we want all the outgoing txs
    outgoing_txs = [tx for tx in txs if is_outgoing_tx(tx, addr)]
    incoming_txs = [tx for tx in txs if not is_outgoing_tx(tx, addr)]

    if depth != 0:
        outgoing_txs = filter(lambda x: x['hash'] in known_txs, outgoing_txs)
        incoming_txs = filter(lambda x: x['hash'] in known_txs, incoming_txs)

        for tx in incoming_txs:
            for obj in tx['out']:
                if obj['hash'] == #function that takes in addr and returns its hash:
                    received[addr] += obj['value']

    for tx in outgoing_txs:
        # Add addresses to the graph
        outgoing_addrs = [x["addr"] for x in tx["out"]]
        addr_map[addr].extend(outgoing_addrs)

        # Get the hash of the every transaction that spent an output.
        tx_hash = tx['hash']
        for next_tx_hash in get_next_tx_hashes(tx_hash):
            known_txs.append(next_tx_hash)

        for x in outgoing_addrs: 
            build_graph(x, depth+1)

def generate_graph():        
    global addr_map
    # Find outgoing transactions

    if 'graph-{}.pkl'.format(DEPTH_LIMIT) in os.listdir('/tmp'):
        with open('/tmp/graph-{}.pkl'.format(DEPTH_LIMIT), 'rb+') as f:
            addr_map = pickle.load(f)
    else:
        with open('suspects.txt', 'r') as f:
            addrs = f.read().split('\n')

        for addr in addrs[:-1]:
            build_graph(addr)

        with open('/tmp/graph-{}.pkl'.format(DEPTH_LIMIT), 'wb+') as f:
            pickle.dump(addr_map, f)

def prob7():
    global addr_map
    def get_labeled_addrs(addr_map):
        if 'labels.pkl' in os.listdir('/tmp'):
            with open('/tmp/labels.pkl','wb+') as f:
                return pickle.load(f)
        else:
            interesting = []
            for addr in addr_map:
                labeled = address_display(addr)
                if addr != labeled:
                    interesting.append(addr)
            with open('/tmp/labels.pkl','rb+') as f:
                pickle.dump(interesting, f)
            return interesting

    for x in get_labeled_addrs(addr_map):
        print(x)

def find_parents(node, visited=[]):
    global addr_map
    
    parents = []
    for k, v in addr_map.items():
        if node in v and k not in visited:
            visited.append(k)
            parents.append(find_parents(k))
    if parents == []:
        return node
    return parents

def prob8():
    global addr_map

    parent_nums = {}
    for k in addr_map:
        parent_nums[k] = len(find_parents(k))
    parent_nums = parent_nums.items()
    parent_nums = sorted(parent_nums, key=lambda x:x[1], reverse=True)
    for x1,x2 in parent_nums:
        print(address_display(x1), x2)
        sleep(0.2)
    print(len(list(filter(lambda x: x[1] > 1, parent_nums))))
    print(len(parent_nums))

if __name__ == '__main__':
    generate_graph()

    prob8()






