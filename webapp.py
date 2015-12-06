from os import listdir as ls
from sys import exit

if 'backend' not in ls('.'):
    print("Are you running this from the root directory?\nAborting!")
    exit(1)

from lib.bottle import route, run, template, get, post, request, view, \
        static_file
from backend.analysis import get_path, get_anonymity_set

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

if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=True)
