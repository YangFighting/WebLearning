#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/10 11:45
# @Author  : ZhangYang
import logging
import re
import socket


def http_send_data(client_socket=None, request_data=None):
    """
        根据请求数据，使用长连接的方式，返回不同的html页面
    :param client_socket:
    :param request_data:
    """
    request_line = request_data.splitlines() if request_data else []

    file_name = "/index.html"
    ret = re.search(r"/(.*) ", request_line[0])
    if ret:
        file_name = ret.group(0)[0:-1]
        if file_name == '/':
            file_name = "/index.html"
    print("file name: {}".format(file_name))

    # http 格式数据 --body
    # noinspection PyBroadException
    try:
        f = open("./html" + file_name, "rb")
        response_body = f.read()
    except Exception as e:
        response_body = "HTTP/1.1 404 NOT FOUND\n"
        response_body += "\n"
        response_body += "------file not found-----"
        response_body = response_body.encode("utf-8")

    # http 格式数据 --header
    response_header = "HTTP/1.1 200 OK\n"
    response_header += "Content-Length:{}\n".format(len(response_body))
    response_header += "\n"

    response = response_header.encode("utf-8") + response_body
    #  返回 http 格式数据给客户端
    client_socket.sendall(response)


def main():
    """ 非阻塞的方式实现并发过程"""
    host = "127.0.0.1"
    port = 7890

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_server_s:
        # 设置服务器先close, 保证端口释放后立即就可以被再次使用
        tcp_server_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 设置 套接字 非阻塞
        tcp_server_s.setblocking(False)
        tcp_server_s.bind((host, port))
        tcp_server_s.listen(3)
        socket_client_list = list()
        while True:
            # time.sleep(0.5)
            try:
                conn_s, client_addr = tcp_server_s.accept()
            except socket.error:
                logging.warning("no accept client")
            except Exception as e:
                logging.error("accept except: {}".format(e.__str__()))
            else:
                logging.warning("accept client_addr: {}".format(client_addr))
                # 设置 套接字 非阻塞
                conn_s.setblocking(False)
                socket_client_list.append(conn_s)

            for socket_client_i in socket_client_list:
                try:
                    recv_data = socket_client_i.recv(1024).decode("utf-8")
                except socket.error:
                    logging.warning("client not recv")
                except Exception as e:
                    logging.error("recv except: {}".format(e.__str__()))
                else:
                    if recv_data:
                        # logging.warning("recv except: {}".format(recv_data))
                        http_send_data(client_socket=socket_client_i, request_data=recv_data)
                    else:
                        socket_client_i.close()
                        socket_client_list.remove(socket_client_i)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [%(levelname)s] %(message)s (%(filename)s:L%(lineno)d)',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filemode='a')
    main()
