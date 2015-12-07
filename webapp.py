from os import listdir as ls
from sys import exit

if 'backend' not in ls('.'):
    print("Are you running this from the root directory?\nAborting!")
    exit(1)

from lib.bottle import route, run, template, get, post, request, view, \
        static_file
from backend.analysis import get_path, get_anonymity_set, test_linkability

@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='./static')

@get('/')
@view('index')
def index():
    return {}

@get('/direct_link')
@view('direct_link')
def direct_link_prompt():
    return {}

@post('/direct_link')
@view('direct_link_results')
def direct_link_handle():
    args = [request.forms.get('tx_in_hash'), 
            request.forms.get('tx_out_hash'), 
            request.forms.get('user_start_addr'),
            request.forms.get('user_end_addr'),
            request.forms.get('mixer_input_addr'),]

    path = get_path(*args)
    print(type(path))

    return {
            "msg"       : "These are linked!" if path else "These are not linked.",
            "path"      : path[:-1] if path else None,
            "last_addr" : path[-1] if path else None
        }

@get('/anonymity_set')
@view('anonymity_set')
def anonymity_set_prompt():
    return {}

@post('/anonymity_set_results')
@view('anonymity_set_results')
def anonymity_set_handle():
    args = [request.forms.get('tx_in_hash'),
            request.forms.get('tx_value'),
            request.forms.get('start_time'),
            request.forms.get('end_time'),
            request.forms.get('flat_fee'),
            request.forms.get('percent_fee_lower'),
            request.forms.get('percent_fee_upper')]

    anonymity_set = get_anonymity_set(*args, verbose=True)
    
    return { 
            "len": len(anonymity_set), 
            "set": anonymity_set
        }

@get('/linkability')
@view('linkability')
def linkability_prompt():
    return {}

@post('/linkability_results')
@view('linkability_results')
def linkability_handle():
    args = [request.forms.get('addr1'), 
            request.forms.get('addr2')]
    
    results = test_linkability(*args)
    for k,v in results.items():
        results[k] = "%.6f" % (float(results[k]), )
        # results[k] = results[k][:results[k].find('.')+6]
        # results[k] += '%'

    return {
        "results": results,
        "namemap": {
            "OverlappingLifespanTest"      : "Lifespan overlap",
            "AverageNumInputsOutputsTest"  : "Average number of inputs and outputs",
            "TransactionFrequencyTest"     : "Transaction frequency",
            "TotalAmountSentReceivedTest"  : "Total bitcoin sent and received",
            "AverageAmountSentReceivedTest": "Average amount sent and received"
        },
        "explanations": {
            "OverlappingLifespanTest"      : """This value represents how much the lifespan of both addresses overlap each other. The lifespan of an address is the number of blocks between that address' first and last transaction.A value close to 1.0 means a nearly complete overlap between the two addresses; a value near 0 means little to no overlap.""",
            "AverageNumInputsOutputsTest"  : "This value compares: 1. the average number of addresses address 1 has sent Bitcoin to in a transaction, and 2. the average number of addresses address 2 has received Bitcoin from in a transaction. A value close to 1.0 means the averages are similar; a value near 0 means the averages are different.",
            "TransactionFrequencyTest"     : "This compares the average frequency of address 1's outgoing transactions to address 2's incoming transactions, where frequency is defined as the total amount of transactions for an address divided by its lifespan. A value close to 1.0 indicates similar frequencies, while a 0.0 shows no correlation between frequencies.",
            "TotalAmountSentReceivedTest"  : "This represents the correlation between the total amount address 1 has sent and address 2 has received. A value close to 1.0 means the amounts are positively correlated; a value close to 0 means they are negatively correlated.",
            "AverageAmountSentReceivedTest": " This represents the correlation between the average amount address 1 sent during a transaction and the average amount address 2 received in a transaction. A value close to 1.0 means they have similar averages, while a 0.0 indicates no similarity."
        }
    }

if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=True)
