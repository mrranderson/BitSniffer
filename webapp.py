from lib.bottle import route, run, template, get, post, request
from backend.analysis import *

@get('/')
def greet():
    return """<a href="/direct_link">Look for direct link</a>"""

@get('/direct_link')
def direct_link_prompt():
    return """
    <form action="/direct_link" method="post">
        tx_in_hash: <input name="tx_in_hash" type="text" /><br/>
        tx_out_hash: <input name="tx_out_hash" type="text" /><br/>
        user_start_addr: <input name="user_start_addr" type="text" /><br/>
        user_end_addr: <input name="user_end_addr" type="text" /><br/>
        mixer_input_addr: <input name="mixer_input_addr" type="text" /><br/>
        <input value="Analyze" type="submit" />
    </form>
    <p>Sample data:</p>
    <p>490898199a566dcb32a4a9cf45cc7d3cb5f1372e1703c90ad7845acf400f17a5</p>
    <p>cb9e8ec8ad02d0edd7b7d9abb85b2312304ffda263493e5ee96e83bc2e78ce17</p>
    <p>1B1tDpsuUBKu25Ktqp8ohziw7qN43FjEQm</p>
    <p>1MV8oVUWVSLTbWDh8p2hof6J7hfnEm4UXM</p>
    <p>1Luke788hdrUcMqdb2sUdtuzcYqozXgh4L</p>
    """

@post('/direct_link')
def direct_link_handle():
    tx_in_hash = request.forms.get('tx_in_hash')
    tx_out_hash = request.forms.get('tx_out_hash')
    user_start_addr = request.forms.get('user_start_addr')
    user_end_addr = request.forms.get('user_end_addr')
    mixer_input_addr = request.forms.get('mixer_input_addr')

    res = direct_link_exists (tx_in_hash, tx_out_hash, user_start_addr,
        user_end_addr, mixer_input_addr)

    print(res)
    if res:
        return "These are linked!"
    return "These are not linked."

run(host='localhost', port=8080, debug=True)
