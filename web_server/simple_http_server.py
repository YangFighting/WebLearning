#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/6 14:25
# @Author  : ZhangYang

import random
import socket
import string


def generate_random_str(random_length=12):
    """
    string.digits = 0123456789
    string.ascii_letters = 26个小写,26个大写
    :param random_length:
    :return:
    """
    # str_list = random.sample(string.digits + string.ascii_letters, random_length)
    str_list = random.sample(string.digits + string.ascii_lowercase.upper(), random_length)
    random_str = ''.join(str_list)
    return random_str


def service_client(client_socket=None, client_addr=None):
    """为客户端返回数据"""
    print("Client Addr: {}".format(client_addr))

    # 1. 接收客户端发送的数据
    request = client_socket.recv(1024)
    print(request.decode("utf-8"))

    # 准备 http 格式数据
    # http 格式数据 --header
    response = "HTTP/1.1 200 OK\n"
    response += "\n"

    response_body = generate_random_str(random_length=12)
    # http 格式数据 --body
    response += "<{0}>{1}</{0}>".format("h1", response_body)

    # 2. 返回 http 格式数据给客户端
    client_socket.send(response.encode("utf-8"))

    #  关闭套接字
    client_socket.close()


def main():
    """ 实现简单的http服务器，向客户端发送固定内容"""
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
            service_client(client_socket=conn_s, client_addr=addr)


if __name__ == '__main__':
    main()
