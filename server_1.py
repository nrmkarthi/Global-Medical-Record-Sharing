from flask import Flask, request
import flask
from subprocess import Popen, PIPE, call

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/get/<key>')
def get(key):
    # fetch off ipfs
    if(key.isalnum()):
        print(key)
        p = Popen(['ipfs', 'cat', key], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate(b" ")
        rc = p.returncode
        resp = flask.Response(output)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    else:
        return 'error'

@app.route('/push', methods=['GET', 'POST'])
def push():
    error = None
    if request.method == 'POST':
        p = Popen(['ipfs', 'add'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate(request.form['data'].encode())
        rc = p.returncode
        resp = flask.Response(output.split(" ")[1])
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    else:
        return 'Invalid request'

@app.route('/test')
def test():
    return '<form action="/push" method="post"><input type="text" name="data"><input type="submit"></form>'
