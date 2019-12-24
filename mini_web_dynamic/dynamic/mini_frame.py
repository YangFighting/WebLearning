#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/20 20:56
# @Author  : ZhangYang

g_url_route = dict()


# 带参数的修饰器
def route(url):
    def decorator(func):
        g_url_route[url] = func

        def warpper(*args, **kwargs):
            return func(*args, **kwargs)

        return warpper

    return decorator


@route("/index.html")
def index():
    with open("./templates/index.html", encoding="utf-8") as f:
        content = f.read()
    return content


@route("/center.html")
def center():
    with open("./templates/center.html", encoding="utf-8") as f:
        return f.read()


def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html;charset=utf-8')])

    file_name = env['PATH_INFO']
    # file_name = "/index.py"

    # if file_name == "/index.py":
    #     return index()
    # elif file_name == "/center.py":
    #     return center()
    # else:
    #     return 'Hello World! 我爱你中国....'
    try:
        return g_url_route.get(file_name)()
    except Exception as e:
        return "route dict key {} error: {}".format(file_name, e.__str__())
