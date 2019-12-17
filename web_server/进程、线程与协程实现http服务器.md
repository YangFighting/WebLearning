# 进程、线程与协程实现 http 服务器

## 进程

使用 multiprocessing 模块，调用如下方法

```python
p = multiprocessing.Process(target=service_client, kwargs={"client_socket": conn_s, "client_addr": addr})
p.start()
conn_s.close()
```

由于进程会复制变量，需要手动关闭socket



## 线程

使用 threading 模块，调用如下方法

```python
t = threading.Thread(target=service_client, args=(conn_s, addr))
t.start()
```



## 协程

```python
from gevent import monkey
monkey.patch_socket()

gevent.spawn(service_client, client_socket=conn_s, client_addr=addr)
```

如果使用 patch_all ，程序会报栈溢出，