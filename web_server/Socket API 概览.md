# Socket API 概览

原文：https://keelii.com/2018/09/24/socket-programming-in-python/



Socket 有一段很长的历史，最初是在 [1971 年被用于 ARPANET](https://en.wikipedia.org/wiki/Network_socket#History)，随后就成了 1983 年发布的 Berkeley Software Distribution (BSD) 操作系统的 API，并且被命名为 [Berkeleysocket](https://en.wikipedia.org/wiki/Berkeley_sockets)

Socket 应用最常见的类型就是 **客户端/服务器** 应用，服务器用来等待客户端的链接。更明确地说，我们将看到用于 [InternetSocket](https://en.wikipedia.org/wiki/Berkeley_sockets) 的 Socket API，有时称为 Berkeley 或 BSD Socket。当然也有 [Unix domain sockets](https://en.wikipedia.org/wiki/Unix_domain_socket) —— 一种用于 **同一主机** 进程间的通信

Python 的 socket 模块提供了使用 Berkeley sockets API 的接口。主要的用到的 Socket API 函数和方法有下面这些：

- `socket()`
- `bind()`
- `listen()`
- `accept()`
- `connect()`
- `connect_ex()`
- `send()`
- `recv()`
- `close()`

##  Socket API 的调用顺序

Socket API 的调用顺序和 TCP 的数据流：

![](https://files.realpython.com/media/sockets-tcp-flow.1da426797e37.jpg)

左边表示服务器，右边则是客户端

服务器创建「监听」Socket 的 API 调用：

- `socket()`
- `bind()`
- `listen()`
- `accept()`

「监听」Socket 会监听客户端的连接，当一个客户端连接进来的时候，服务器将调用 `accept()` 来「接受」或者「完成」此连接

客户端调用 `connect()` 方法来建立与服务器的链接，并开始三次握手。

客户端和服务器的数据交换过程，调用 `send()` 和 `recv()`方法

客户端和服务器调用 `close()` 方法来关闭各自的 socket



## 简单的服务端程序

```python
#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # 标准的回环地址 (localhost)
PORT = 65432        # 监听的端口 (非系统级的端口: 大于 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
```

### socket.socket()

`socket.socket()` 创建了一个 socket 对象，可以使用 [with 语句](https://docs.python.org/3/reference/compound_stmts.html#with)，这样你就不用再手动调用 `s.close()` 来关闭 socket 了

```python
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    pass  # Use the socket object without calling s.close().
```

调用 `socket()` 时传入的 socket 地址族参数 `socket.AF_INET` 表示因特网 IPv4 [地址族](https://realpython.com/python-sockets/#socket-address-families)，`SOCK_STREAM` 表示使用 TCP 的 socket 类型，协议将被用来在网络中传输消息

`bind()` 用来关联 socket 到指定的网络接口（IP 地址）和端口号

```python
HOST = '127.0.0.1'
PORT = 65432

# ...

s.bind((HOST, PORT))
```

### bind()

`bind()` 方法的入参取决于 socket 的地址族，`socket.AF_INET` (IPv4)，它将返回两个元素的元组：(host, port)

host 可以是主机名称、IP 地址、空字符串，如果使用 IP 地址，host 就应该是 IPv4 格式的字符串，`127.0.0.1` 是标准的 IPv4 回环地址，只有主机上的进程可以连接到服务器，如果你传了空字符串，服务器将接受本机所有可用的 IPv4 地址

端口号应该是 1-65535 之间的整数（0是保留的），这个整数就是用来接受客户端链接的 TCP 端口号，如果端口号小于 1024，有的操作系统会要求管理员权限



### listen()

`listen()` 方法调用使服务器可以接受连接请求，这使它成为一个「监听中」的 socket

```python
s.listen()
conn, addr = s.accept()
```

`listen()` 方法有一个 `backlog` 参数。它指定在拒绝新的连接之前系统将允许使用的 *未接受的连接* 数量

如果你的服务器需要同时接收很多连接请求，增加 backlog 参数的值可以加大等待链接请求队列的长度，最大长度取决于操作系统。



### accept()

`accept()` 方法**阻塞并等待传入连接**。当一个客户端连接时，它将返回一个**新的** **socket 对象**，对象中有表示当前连接的 conn 和一个由主机、端口号组成的 IPv4/v6 连接的元组，更多关于元组值的内容可以查看 [socket 地址族](https://keelii.com/2018/09/24/socket-programming-in-python/#socket 地址族) 一节中的详情

```python
conn, addr = s.accept()
with conn:
    print('Connected by', addr)
    while True:
        data = conn.recv(1024)
        if not data:
            break
        conn.sendall(data)
```

 `accept()` 获取客户端 socket 连接对象 conn 后，使用一个无限 while 循环来阻塞调用 `conn.recv()`，无论客户端传过来什么数据都会使用 `conn.sendall()` 打印出来

如果 `conn.recv()` 方法返回一个空 byte 对象（`b''`），然后客户端关闭连接，循环结束，with 语句和 conn 一起使用时，通信结束的时候会自动关闭 socket 链接



### send() 与 sendall()

使用`send()`进行发送的时候，`Python`将内容传递给系统底层的`send`接口，也就是说，`Python`并不知道这次调用是否会全部发送完成，比如最大传输单元（`Maximum Transmission Unit，MTU`）是1500，但是此次发送的内容是2000，那么除了包头等等其他信息占用，发送的量可能在1000左右，还有1000未发送完毕，但是，`send()`不会继续发送剩下的包，因为它**只会发送一次**，发送成功之后会**返回此次发送的字节数**，会返回数字1000给用户，然后就结束了，如果需要将剩下的1000发送完毕，**需要用户自行获取返回结果**，然后将内容剩下的部分继续调用`send()`进行发送

`sendall()`是对`send()`的包装，完成了用户需要手动完成的部分，它会自动判断每次发送的内容量，然后从总内容中删除已发送的部分，将剩下的继续传给`send()`进行发送