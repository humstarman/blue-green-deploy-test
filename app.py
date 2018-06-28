#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
import os
import hashlib
import json
from hashlib import sha256
from time import time, asctime
from uuid import uuid4
from textwrap import dedent
from uuid import uuid4
from flask import Flask, jsonify, request, render_template
from urllib.parse import urlparse
import requests
import pickle
from optparse import OptionParser
 
def parse_opts(parser):
    parser.add_option("-p","--port",action="store",type="int",dest="port",default=8080,help="the working port")
    parser.add_option("--host",action="store",type="string",dest="host",default="",help="the host ip, where the app resides on")
    parser.add_option("--pod",action="store",type="string",dest="pod",default="",help="pod ip")
    (options,args) = parser.parse_args()

    return options

options = parse_opts(OptionParser(usage="%prog [options]"))
# Instantiate our Node
app = Flask(__name__)
app.secret_key = os.urandom(24) 
# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')
# Instantiate the Blockchain
fn = os.path.join("/mnt","demo.dat") 
def ret_id(ip):
    if ip == "172.31.78.215": return "1"
    if ip == "172.31.78.216": return "2"
    if ip == "172.31.78.217": return "3"
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    if os.path.exists(fn):
        with open(fn,'r') as f:
            n = (f.readlines())[0].replace('\n','')
    response = {
        'host': options.host,
        'pod': options.pod,
        'id': ret_id(options.host),
        'n': n
    }
    return render_template('index.html', ret=response) 
@app.route('/healthz', methods=['GET'])
def healthz():
    response = {
        'status': "normal",
        'time': str(asctime()),
    }
    return jsonify(response), 200
@app.route('/add', methods=['GET'])
def add():
    if os.path.exists(fn):
        with open(fn,'r') as f:
            n = (f.readlines())[0].replace('\n','')
    n = str(int(n) + 1)
    with open(fn,'w') as f:
        f.write(n)
    response = {
        'host': options.host,
        'pod': options.pod,
        'id': ret_id(options.host),
        'n': n
    }
    return render_template('index.html', ret=response) 
@app.route('/reset', methods=['GET'])
def reset():
    n = str(0)
    with open(fn,'w') as f:
        f.write(n)
    response = {
        'host': options.host,
        'pod': options.pod,
        'id': ret_id(options.host),
        'n': n
    }
    return render_template('index.html', ret=response) 
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=options.port)
