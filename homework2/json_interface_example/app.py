#!/usr/bin/env python3
# coding:utf-8
import os
import sys

from flask import Flask

from calculate.cal import bp

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
if __name__ == '__main__':
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['JSON_AS_ASCII']=False
    app.register_blueprint(bp)
    app.run(host='0.0.0.0',port=4999,debug=True)#联机操作
    #app.run()