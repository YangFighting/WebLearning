#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/20 17:56
# @Author  : ZhangYang
import json
import re
import socket
import sys
import threading


class WSGIServer(object):
    def __init__(self, static_path, app):
        self.host = "127.0.0.1"
        self.port = 7890
        self.status = None
        self.headers = None
        self.application = app
        self.static_path = static_path

        # 建立服务端 socket
        self.server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 绑定
        self.server_s.bind((self.host, self.port))

        # 监听
        self.server_s.listen(10)

    def __del__(self):
        self.server_s.close()

    def server_client(self, client_socket):
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
                f = open(self.static_path + file_name, "rb")
                response_body = f.read()
            except Exception as e:
                response_body = "HTTP/1.1 404 NOT FOUND\n"
                response_body += "\n"
                response_body += "------file not found-----"
                response_body = response_body.encode("utf-8")

            response_header = "HTTP/1.1 200 OK\n"
            response_header += "Content-Length:{}\n".format(len(response_body))
            response_header += "\n"

            # 2. 返回 http 格式数据给客户端
            client_socket.sendall(response_header.encode("utf-8"))
            client_socket.sendall(response_body)
        else:
            # 动态请求
            env = dict()
            env["PATH_INFO"] = file_name
            # start_response =
            response_body = self.application(env, self.set_response_header)
            response_body = response_body.encode("utf-8")

            # http 格式数据 --header
            response_header = "HTTP/1.1 {}\n".format(self.status)

            for header_i in self.headers:
                response_header += "{}:{}\n".format(header_i[0], header_i[1])
            response_header += "Content-Length:{}\n".format(len(response_body))
            response_header += "\n"

            # 2. 返回 http 格式数据给客户端
            client_socket.sendall(response_header.encode("utf-8"))
            client_socket.sendall(response_body)

    def set_response_header(self, status, headers):
        self.status = status
        self.headers = [("server", "mini_web v8.8")]
        self.headers += headers

    def run_server(self):
        while True:
            # 建立客户端连接
            conn_s, addr = self.server_s.accept()
            t = threading.Thread(target=self.server_client, args=(conn_s,))
            t.start()


def main():

    # web 服务器配置文件
    with open("./web_server.conf", 'r', encoding="utf-8") as f:
        conf_info = json.load(f)
    frame_name = "mini_frame"
    app_name = "application"

    sys.path.append(conf_info['dynamic_path'])
    frame = __import__(frame_name)
    app = getattr(frame, app_name)
    wsgi_server = WSGIServer(conf_info['static_path'], app)
    wsgi_server.run_server()


if __name__ == "__main__":
    main()
