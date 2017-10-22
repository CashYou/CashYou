from flask import Flask, request
from flask import render_template
from bokeh.embed import components
from stock_gatherer import StockGatherer
from dataStorage import *
import os
app = Flask(__name__)

@app.route('/')
def index():
    # change lager
    return render_template('elate/index.html')

@app.route('/portal/')
def portal():
    '''if request.method == 'POST':
        user = request.data'''
    return render_template('elate/portal.html')

@app.route('/stocks/', methods=['POST', 'GET'])
def stocks():
    '''if request.method == 'POST':
        user = request.data'''
    error = None
    script = ' '
    if request.method == 'POST': # and "testButton" in request.POST:
        result = request.form
        for key, val in result.items():
            if key == 'group':
                group = val
        if group == '':
            error = 'Please choose a group.'
            script = ' '
            div = {}
        else:
            full_site = pickle.load(open("ALL_GROUPS.p", "rb"))
            info = full_site.investGroups[int(group)].getInfo()
            groupname = full_site.investGroups[int(group)].name
            advisor = full_site.investGroups[int(group)].getAdvisors()[0].name

    return render_template('elate/stocks.html', group=group, error=error,
                           info=info, advisor=advisor, groupname=groupname)

#TODO: Implement this
@app.route('/join/', methods=['POST', 'GET'])
def join():
    pass


@app.route('/result/', methods=['POST', 'GET'])
def result():
    error = None
    script = ''
    div = {}
    if request.method == 'POST': # and "testButton" in request.POST:
        result = request.form
        for key, val in result.items():
            if key == 'prod':
                prod = val

        if prod == '': # checks to see if user filled everything in
            error = 'Please choose a company.'
            script = ' '
            div = {}
            cheapest_dates = ""
        else: #checks to see if input is a number and in the proper range
            gatherer = StockGatherer()
            plot = gatherer.getGraph(prod)
            script, div = components(plot)
    return render_template("elate/result.html", prod=prod,
                         error=error, script=script, div=div)

if __name__ == '__main__':
    HOST = '0.0.0.0' if 'PORT' in os.environ else '127.0.0.1'
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host=HOST, port=PORT)
    #app.run()
