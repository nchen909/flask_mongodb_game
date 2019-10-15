#!/usr/bin/env python3

from flask import Blueprint
from flask import jsonify
from flask import request

bp = Blueprint("mul", __name__, url_prefix="/cal")


@bp.route("/<string:cmd>/<int:x>/<int:y>", methods=['GET'])
def cal_get(cmd, x, y):
    result, ok = cal_gut(cmd, x, y)
    return jsonify({"result": result, "ok": ok})


@bp.route("/json", methods=["POST"])
def cal_post():
    result, ok = cal_gut(request.json["cmd"], request.json["op1"], request.json["op2"])
    return jsonify({"result": result, "ok": ok})


def cal_gut(cmd, x, y):
    if cmd == "add":
        return x + y, True
    elif cmd == "sub":
        return x - y, True
    elif cmd == "mul":
        return x * y, True
    elif cmd == "div":
        return int(x / y), True
    else:
        return 0, False
