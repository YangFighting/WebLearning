#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/20 20:56
# @Author  : ZhangYang
import re
import urllib

from pymysql import *

g_url_route = dict()

import logging

# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关

# 第二步，创建一个handler，用于写入日志文件
logfile = './log.txt'
fh = logging.FileHandler( logfile, mode='a', encoding='utf-8' )  # open的打开模式这里可以进行参考
fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关

# 第三步，再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)   # 输出到console的log等级的开关

# 第四步，定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 第五步，将logger添加到handler里面
logger.addHandler(fh)
logger.addHandler(ch)


# 带参数的修饰器
def route(url):
    def decorator(func):
        g_url_route[url] = func

        def warpper(*args, **kwargs):
            return func(*args, **kwargs)

        return warpper

    return decorator


@route("/index.html")
def index(ret):
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
def center(ret):
    with open("./templates/center.html", encoding="utf-8") as f:
        content = f.read()

    # 创建Connection连接
    conn = connect(host='47.97.124.83', port=3306, database='stock_db', user='root', password='123456',
                   charset='utf8')

    # 获得Cursor对象
    cs = conn.cursor()

    # 执行select语句，并返回受影响的行数：查询一条数据
    cs.execute(
        """select i.code, i.short, i.chg, i.turnover, i.price, i.highs, f.note_info from focus as f inner join info as i on f.info_id = i.id;""" )
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


@route(r"/add/(\d+)\.html")
def add_focus(ret):

    # 获取股票代码
    stock_code = ret.group(1)
    # 判断 股票代码 是否存在
    conn = connect(host='47.97.124.83', port=3306, database='stock_db', user='root', password='123456',
                   charset='utf8')
    cs = conn.cursor()
    sql = """select * from info where code=%s;"""
    # 防止SQL注入
    cs.execute( sql, (stock_code,) )
    if not cs.fetchall():
        cs.close()
        conn.close()
        return "股票代码不存在"
    # 判断 股票是否已经关注过
    sql = """ select * from info as i inner join focus as f on i.id=f.info_id where i.code=%s;"""
    cs.execute(sql, (stock_code,))
    if cs.fetchone():
        cs.close()
        conn.close()
        return "已经关注过了，请勿重复关注..."

    # 4. 添加关注
    sql = """insert into focus (info_id) select id from info where code=%s;"""
    cs.execute(sql, (stock_code,))
    conn.commit()
    cs.close()
    conn.close()
    return "关注成功！"


@route(r"/del/(\d+)\.html")
def del_focus(ret):

    # 获取股票代码
    stock_code = ret.group(1)
    # 判断 股票代码 是否存在
    conn = connect(host='47.97.124.83', port=3306, database='stock_db', user='root', password='123456',
                   charset='utf8')
    cs = conn.cursor()
    sql = """select * from info where code=%s;"""
    # 防止SQL注入
    cs.execute( sql, (stock_code,) )
    if not cs.fetchall():
        cs.close()
        conn.close()
        return "股票代码不存在"
    # 判断 股票是否已经关注过
    sql = """ select * from info as i inner join focus as f on i.id=f.info_id where i.code=%s;"""
    cs.execute(sql, (stock_code,))
    if not cs.fetchone():
        cs.close()
        conn.close()
        return "还未关注，请勿取消关注 %s..." % stock_code

    # 取消关注
    sql = """delete from focus where info_id = (select id from info where code=%s);"""
    cs.execute(sql, (stock_code,))
    conn.commit()
    cs.close()
    conn.close()
    return "取消关注成功！"


@route(r"/update/(\d+)\.html")
def show_update_page(ret):
    """显示修改的那个页面"""
    # 1. 获取股票代码
    stock_code = ret.group(1)

    # 2. 打开模板
    with open("./templates/update.html", encoding="utf-8") as f:
        content = f.read()

    # 3. 根据股票代码查询相关的备注信息
    conn = connect(host='47.97.124.83', port=3306, database='stock_db', user='root', password='123456',
                   charset='utf8')
    cs = conn.cursor()
    sql = """select f.note_info from focus as f inner join info as i on i.id=f.info_id where i.code=%s;"""
    cs.execute(sql, (stock_code,))
    stock_infos = cs.fetchone()
    note_info = stock_infos[0]  # 获取这个股票对应的备注信息
    cs.close()
    conn.close()

    content = re.sub(r"\{%note_info%\}", note_info, content)
    content = re.sub(r"\{%code%\}", stock_code, content)

    return content


@route(r"/update/(\d+)/(.*)\.html")
def save_update_page(ret):
    """"保存修改的信息"""
    stock_code = ret.group(1)
    comment = ret.group(2)
    comment = urllib.parse.unquote(comment)

    conn = connect(host='47.97.124.83', port=3306, database='stock_db', user='root', password='123456',
                   charset='utf8')
    cs = conn.cursor()
    sql = """update focus set note_info=%s where info_id = (select id from info where code=%s);"""
    cs.execute( sql, (comment, stock_code) )
    conn.commit()
    cs.close()
    conn.close()

    return "修改成功..."


def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html;charset=utf-8')])

    file_name = env['PATH_INFO']
    logging.info( "访问的是: %s" % file_name )
    # file_name = "/index.py"

    # if file_name == "/index.py":
    #     return index()
    # elif file_name == "/center.py":
    #     return center()
    # else:
    #     return 'Hello World! 我爱你中国....'
    try:
        for url, func in g_url_route.items():
            ret = re.match(url, file_name)
            if ret:
                return func(ret)
        else:
            logging.warning( "没有对应的函数...." )
            return "没有访问的页面--->%s" % file_name
    except Exception as e:
        return "route dict key {} error: {}".format(file_name, e.__str__())
