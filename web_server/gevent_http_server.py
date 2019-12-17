#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/9 16:54
# @Author  : ZhangYang


import re
import socket

import gevent
from gevent import monkey

monkey.patch_socket()
# monkey.patch_all()


def service_client(client_socket=None, client_addr=None):
    """为客户端返回数据"""

    # 1. 接收客户端发送的数据
    request = client_socket.recv(1024).decode("utf-8")
    request_line = request.splitlines() if request else []
    if not request_line:
        #  关闭套接字
        client_socket.close()
        return
    print("request header: {}".format(request_line[0]))

    file_name = "/index.html"
    ret = re.search(r"/(.*) ", request_line[0])
    if ret:
        file_name = ret.group(0)[0:-1]
        if file_name == '/':
            file_name = "/index.html"
    print("file name: {}".format(file_name))

    # 准备 http 格式数据
    # http 格式数据 --header
    response = "HTTP/1.1 200 OK\n"
    response += "\n"

    # http 格式数据 --body
    with open("./html" + file_name, "rb") as f:
        response_body = f.read()

    # 2. 返回 http 格式数据给客户端
    client_socket.sendall(response.encode("utf-8"))
    client_socket.sendall(response_body)

    #  关闭套接字
    client_socket.close()


def main():
    """ 使用 多协程 完成实现简单的http服务器"""
    host = ''
    port = 7890

    # 建立套接字
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_server_s:
        # 设置服务器先close, 保证端口释放后立即就可以被再次使用
        tcp_server_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 绑定端口
        tcp_server_s.bind((host, port))
        # 监听客户端
        tcp_server_s.listen(3)
        while True:
            # 建立客户端连接
            conn_s, addr = tcp_server_s.accept()
            # 为客户端服务
            gevent.spawn(service_client, client_socket=conn_s, client_addr=addr)


if __name__ == '__main__':
    main()
