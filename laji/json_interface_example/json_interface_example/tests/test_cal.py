#!/usr/bin/env python3
import random

from flask.testing import FlaskClient

commands = ["add", "sub", "mul", "div", "no"]


def verify_json(json, cmd: str, x: int, y: int):
    result = 0
    ok = True
    if cmd == "add":
        result = x + y
    elif cmd == "sub":
        result = x - y
    elif cmd == "mul":
        result = x * y
    elif cmd == "div":
        result = int(x / y)
    else:
        ok = False
    assert json["ok"] is ok
    assert json["result"] == result


def test_cal_get(client: FlaskClient):
    for cmd in commands:
        op1 = random.randint(0, 100)
        op2 = random.randint(1, 100)
        response = client.get("/cal/%s/%d/%d" % (cmd, op1, op2))
        json = response.get_json()
        verify_json(json, cmd, op1, op2)


def test_cal_post(client: FlaskClient):
    for cmd in commands:
        op1 = random.randint(0, 100)
        op2 = random.randint(1, 100)
        response = client.post('/cal/json', json=dict(
            cmd=cmd,
            op1=op1,
            op2=op2))
        json = response.get_json()
        verify_json(json, cmd, op1, op2)
