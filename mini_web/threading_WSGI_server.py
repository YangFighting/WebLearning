#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/17 20:07
# @Author  : ZhangYang
import datetime
import threading
import re
import socket


class WSGIServer(object):
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 7890

    @staticmethod
    def service_client(client_socket=None):
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

        # http 格式数据 --body
        if not file_name.endswith(".py"):
            # noinspection PyBroadException
            try:
                f = open("./html" + file_name, "rb")
                response_body = f.read()
            except Exception as e:
                response_body = "HTTP/1.1 404 NOT FOUND\n"
                response_body += "\n"
                response_body += "------file not found-----"
                response_body = response_body.encode("utf-8")
        else:
            response_body = "time:{}".format(datetime.datetime.now())
            response_body = response_body.encode("utf-8")

        # http 格式数据 --header
        response_header = "HTTP/1.1 200 OK\n"
        response_header += "Content-Length:{}\n".format(len(response_body))
        response_header += "\n"

        # 2. 返回 http 格式数据给客户端
        client_socket.sendall(response_header.encode("utf-8"))
        client_socket.sendall(response_body)

    def run_server(self):
        """ 使用 多进程 完成实现简单的http服务器"""

        # 建立套接字
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_server_s:
            # 设置服务器先close, 保证端口释放后立即就可以被再次使用
            tcp_server_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # 绑定端口
            tcp_server_s.bind((self.host, self.port))
            # 监听客户端
            tcp_server_s.listen(3)
            while True:
                # 建立客户端连接
                conn_s, addr = tcp_server_s.accept()
                # 为客户端服务
                t = threading.Thread(target=WSGIServer.service_client, args=(conn_s,))
                t.start()


if __name__ == '__main__':
    wsgi_server = WSGIServer()
    wsgi_server.run_server()
