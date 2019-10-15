#!/usr/bin/env python3

from flask import Flask
from flask import Blueprint
from flask import jsonify
from flask import request

if __name__ == '__main__':

    app = Flask(__name__)
    app.register_blueprint(bp)
    app.run(debug=True)