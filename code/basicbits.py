from flask import (Blueprint, render_template, render_template_string, request, redirect, Markup, jsonify)
import json
import urllib
import requests


#debug enable for logging
app_set_debug_mode = 0 # 0=none,1=entry,2=entry/exit,3=all

######################################################################
#  Application routing and web end
######################################################################

bp = Blueprint('basicbits', __name__, url_prefix = '/basicbits')

# route/render the home page
@bp.route('/home', methods = ('GET', 'POST'))
def render_home():
    if request.method == 'GET':
        return render_template('basicbits/basicbits.tmpl.html', basicbitsanswer="home!")

# api requests, returns json
@bp.route('/api', methods = ('GET', 'POST'))
def serve_api_request():
    if request.method == 'GET':
        return jsonify( api_handle_basicbits_message( request  ) )
    
# route and render the results (we're subbing back to the index with extra data)
# might want to consider changing this to a template on its own down the road
@bp.route('/search', methods = ('GET', 'POST'))
def render_search():
    if request.method == 'GET':
        return handle_basicbits_message( request ) 


######################################################################
#  Setup basicbits and define helper function
######################################################################

basicbits_data_folder = "static/data/can-live/"

# pull in the json file and load it for use
def get_basicbits_db_json(answerfile):
    with open(basicbits_data_folder+answerfile+'.json') as f:
        data = json.load(f)
        return data

# setup some basicbits answers
basicbits_db = get_basicbits_db_json('basicbits-en');
    
# the api return as json response, this can be used for whatever application you like
def api_handle_basicbits_message(request):
    basic_bits_answer = {"basicbits_answer": request}
    return basic_bits_answer

# regular response, returns html to the render
def handle_basicbits_message(request,render_template_target=None):
    if render_template_target is None:
        render_template_target = 'basicbits/basicbits.tmpl.html'

    #debug
    if app_set_debug_mode >= 1: 
        print(f"-- bb -- > handle_basicbits_message > enter > {request} {render_template_target}")

    text = request.args.get('basicbits_ask', False)
    lang = request.args.get('recognition_language', False)
    tlx = request.args.get('recognition_lang_tlxd', False)
    if not text:
        text = "basicbits is waiting for your input"
    if not lang:
        lang = "en-US"
    if not tlx:
        tlx = "disabled"
    
    if lang == "fr-CA":
        if tlx == "enabled":
            pass 
    
    q = basicbits_db['bbjsonfield']
    basicbits_answer = text + " " + lang + " " + tlx + " " + q

    return render_template(render_template_target, basicbitsanswer=basicbits_answer)

