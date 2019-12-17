#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/9 21:15
# @Author  : ZhangYang
import datetime
import logging
import socket
import threading

ERROR_COUNT = 0


def main():
    """ socket 客户端， 用于测试服务端"""
    global ERROR_COUNT
    # host = "10.91.21.140"
    host = "127.0.0.1"
    port = 7890
    n = 1000
    threads_list = list()
    for i in range(1, n):
        t = threading.Thread(target=http_client, args=(host, port))
        threads_list.append(t)
        t.start()
    for threads_i in threads_list:
        threads_i.join()
    logging.warning("线程运行错误个数：{}".format(ERROR_COUNT))


def http_client(host=None, port=None):
    global ERROR_COUNT
    start_time = datetime.datetime.now()
    socket_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        socket_c.connect((host, port))
        request = "GET / HTTP/1.1"
        socket_c.send(request.encode("utf-8"))
        socket_c.recv(1024)
    except Exception as e:
        ERROR_COUNT +=1
        logging.error(e.__str__())

    end_time = datetime.datetime.now()
    time = (end_time - start_time).seconds
    logging.warning("线程运行时间：{}s".format(time))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [%(levelname)s] %(message)s (%(filename)s:L%(lineno)d)',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filemode='a')
    main()
