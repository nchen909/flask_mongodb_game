#!/usr/bin/env python3

import os
import sys

from flask import Flask

from calculate.cal import bp

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

if __name__ == '__main__':
    app = Flask(__name__)
    app.register_blueprint(bp)
    app.run(debug=True)