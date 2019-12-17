# str 与 bytes 的区别



bytes 对象以二进制形式记录对象，至于对象具体表示什么，则由相应的编码格式解码所决定

bytes 是 Python 3中特有的，

- **str** 使用**encode**方法 转化为**bytes**
- **bytes**使用**decode**方法转化为**str**

而在 Python 2 里将bytes视为str，所以Python2中可以直接通过encode()和decode()方法进行编码解码，而在Python3中，需要编解码的类型

