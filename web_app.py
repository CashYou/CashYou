from flask import Flask
from flask import render_template
import os.environ
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
     HOST = '0.0.0.0' if 'PORT' in os.environ else '127.0.0.1'
     PORT = int(os.environ.get('PORT', 5000)))
     app.run(host=HOST, port=PORT)
