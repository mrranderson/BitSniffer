from os import listdir as ls
from sys import exit

if 'backend' not in ls('.'):
    print("Are you running this from the root directory?\nAborting!")
    exit(1)

from lib.bottle import route, run, template, get, post, request, view, \
        static_file
import backend.analysis

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
def direct_link_handle():
    tx_in_hash = request.forms.get('tx_in_hash')
    tx_out_hash = request.forms.get('tx_out_hash')
    user_start_addr = request.forms.get('user_start_addr')
    user_end_addr = request.forms.get('user_end_addr')
    mixer_input_addr = request.forms.get('mixer_input_addr')

    res = backend.direct_link_exists (tx_in_hash, tx_out_hash, user_start_addr,
        user_end_addr, mixer_input_addr)

    print(res)
    if res:
        return "These are linked!"
    return "These are not linked."

@get('/anonymity_set')
@view('anonymity_set')
def anonymity_set_prompt():
    return {}

@post('/anonymity_set')
def anonymity_set_handle():
    tx_in_hash = request.forms.get('tx_in_hash')
    tx_out_hash = request.forms.get('tx_out_hash')
    user_start_addr = request.forms.get('user_start_addr')
    user_end_addr = request.forms.get('user_end_addr')
    mixer_input_addr = request.forms.get('mixer_input_addr')
    start_time = request.forms.get('start_time')
    end_time = request.forms.get('end_time')
    #amount_mixed = request.forms.get('amount_mixed')
    flat_fee = request.forms.get('flat_fee')
    percent_fee_lower = request.forms.get('percent_fee_lower')
    percent_fee_upper = request.forms.get('percent_fee_upper')
 
    anonymity_set = backend.get_anonymity_set(tx_in_hash, tx_out_hash, user_start_addr,
        user_end_addr, mixer_input_addr, start_time, end_time, flat_fee, percent_fee_lower, percent_fee_upper)

    print(anonymity_set)
    return "There are %d transactions in the anonymity set." % len(anonymity_set)


if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)
