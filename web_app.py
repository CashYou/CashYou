from flask import Flask
from flask import render_template
from stock_gatherer import StockGatherer
import os
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('elate/index.html')

@app.route('/portal/')
def portal():
    '''if request.method == 'POST':
        user = request.data'''
    return render_template('elate/portal.html')

@app.route('/result/', methods=['POST', 'GET'])
def result():
    error = None
    script = ''
    div = {}
    if request.method == 'POST':
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
    return render_template("result.html", prod=prod,
                         error=error, script=script, div=div)

if __name__ == '__main__':
     HOST = '0.0.0.0' if 'PORT' in os.environ else '127.0.0.1'
     PORT = int(os.environ.get('PORT', 5000))
     app.run(host=HOST, port=PORT)
