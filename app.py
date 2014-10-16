from flask import Flask
from flask import request
from dlt17500 import Tdlt, dispatch_data

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>Home</h1>'

@app.route('/getdata/dlt/<int:qh>', methods=['GET'])
def signin_form(qh):
    return dispatch_data(qh)

if __name__ == '__main__':
    app.run()