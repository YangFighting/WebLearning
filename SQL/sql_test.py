from pymysql import *


def main():
    # 创建Connection连接
    conn = connect(host='47.97.124.83', port=3306, database='jingdong', user='root', password='123456', charset='utf8')

    # 获得Cursor对象
    cs1 = conn.cursor()

    # 执行select语句，并返回受影响的行数：查询一条数据
    count = cs1.execute("""select id,name from goods where id>=4""")

    # 打印受影响的行数
    print("查询到%d条数据:" % count)

    # 关闭Cursor对象
    cs1.close()
    # 关闭Connection对象
    conn.close()


if __name__ == "__main__":
    main()
