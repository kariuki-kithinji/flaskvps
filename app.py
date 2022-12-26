import json
from flask import Flask, render_template, jsonify, request, url_for, redirect
from datetime import timedelta
import os
from subprocess import PIPE, Popen

import requests as req
#from flaskwebgui import FlaskUI

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days = 7)

#ui = FlaskUI(app, width=500, height=500) 

@app.route('/execute/cmd.<command>', methods=['POST', 'GET'])
def execute(command):
    try:
        p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        if len(stdout) == 0 and len(stderr) > 0:
            return stderr
        return stdout
        
    except Exception as e:
        return e

@app.route('/info', methods=['POST', 'GET'])
def info():
    ip = str(req.get("http://flask-proxy-demo.herokuapp.com/").text)
    addr = ip.split(" ")[len(ip.split(" "))-1].strip()
    info = req.get("http://ip-api.com/json/{}".format(addr)).json()
    return (ip,json.dumps(info, indent=2))

@app.route('/', methods=['POST', 'GET'])
def terminal():
    path = os.path.abspath(os.getcwd())
    return render_template('index.html',path=path)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)


