from pymysql import *
import psycopg2


def connet_mysql():
    # 创建Connection连接
    conn = connect( host='ip', port=3306, database='jingdong', user='root', password='password',
                    charset='utf8' )

    # 获得Cursor对象
    cs1 = conn.cursor()

    # 执行select语句，并返回受影响的行数：查询一条数据
    count = cs1.execute( """select * from goods""" )

    # 打印受影响的行数
    print( "查询到%d条数据:" % count )

    # 关闭Cursor对象
    cs1.close()
    # 关闭Connection对象
    conn.close()


def main():
    # 连接mysql
    connet_mysql()


if __name__ == "__main__":
    main()
