#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/20 20:56
# @Author  : ZhangYang
import re
from pymysql import *

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

    # 创建Connection连接
    conn = connect(host='47.97.124.83', port=3306, database='stock_db', user='root', password='123456',
                   charset='utf8')

    # 获得Cursor对象
    cs = conn.cursor()

    # 执行select语句，并返回受影响的行数：查询一条数据
    cs.execute("""select * from info;""")
    stock_info = cs.fetchall()
    cs.close()
    conn.close()

    html_template  = """
        <tr>
            <td>{0}</td>
            <td>{1}</td>
            <td>{2}</td>
            <td>{3}</td>
            <td>{4}</td>
            <td>{5}</td>
            <td>{6}</td>
            <td>{7}</td>
            <td>
                <input type="button" value="添加" id="toAdd" name="toAdd" systemidvaule="%s">
            </td>
        </tr>
    """
    # html = html_template.format(1, "004", "", "", "", "", "", "")
    html = ""
    for info_i in stock_info:
        html += html_template.format(*info_i)

    content = re.sub(r"\{%content%\}", str(html), content)
    return content


@route("/center.html")
def center():
    with open("./templates/center.html", encoding="utf-8") as f:
        content = f.read()

    # 创建Connection连接
    conn = connect(host='47.97.124.83', port=3306, database='stock_db', user='root', password='123456',
                   charset='utf8')

    # 获得Cursor对象
    cs = conn.cursor()

    # 执行select语句，并返回受影响的行数：查询一条数据
    cs.execute(
        """select i.code, i.short, i.chg, i.turnover, i.price, i.highs, f.note_info from focus as f inner join info as i on f.info_id = i.id;""")
    stock_info = cs.fetchall()
    cs.close()
    conn.close()

    html_template = """
       <tr>
           <td>{0}</td>
           <td>{1}</td>
           <td>{2}</td>
           <td>{3}</td>
           <td>{4}</td>
           <td>{5}</td>
           <td>{6}</td>
           <td>
               <a type="button" class="btn btn-default btn-xs" href="/update/%s.html"> <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 修改 </a>
           </td>
           <td>
               <input type="button" value="删除" id="toDel" name="toDel" systemidvaule="%s">
           </td>
       </tr>
    """
    # html = html_template.format(1, "004", "", "", "", "", "")
    html = ""
    for info_i in stock_info:
        html += html_template.format(*info_i)

    content = re.sub(r"\{%content%\}", str(html), content)
    return content

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
