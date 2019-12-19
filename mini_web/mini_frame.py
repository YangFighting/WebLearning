#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/18 20:56
# @Author  : ZhangYang


def application(environ=None, start_response=None):
    start_response("200 OK", [('Content-Type', 'text/html;charset=utf-8')])
    return 'Hello World! 我爱你中国....'
