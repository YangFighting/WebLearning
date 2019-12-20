#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/18 20:56
# @Author  : ZhangYang


def index():
    return "这是主页"


def login():
    return "这是登录页"


def application(environ=None, start_response=None):
    start_response("200 OK", [('Content-Type', 'text/html;charset=utf-8')])
    if environ.get("PATH_INFO") == "/index.py":
        return index()
    elif environ.get("PATH_INFO") == "/login.py":
        return login()
    else:
        return 'Hello World! 我爱你中国....'
