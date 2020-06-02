# 获取所有的 PaperInfo 表的信息 格式化后传回前端

import pymysql


# 获取所有的 PaperInfo 表的信息 格式化后传回前端
def get_Modify_PaperInfoFromMySql():
    # 答卷 [{'id': 1, 'title': 'first paper', 'author':'first author', 'abstract':'abs1..', 'tobeadd':'...'},
    ans = []

    conn = pymysql.connect(host="localhost", user="root", password="root", database="paperinfo")
    cursor = conn.cursor()
    sql = "select * from paperinfo"
    cursor.execute(sql)
    getFromMySql = cursor.fetchall()
    # ((ID,title, author, abstract, localAddress)      , ())
    print("数据库中的数据总量：", len(getFromMySql))
    for item in getFromMySql:
        temp = {'id':item[0], 'title':item[1], 'author':item[2], 'abstract':item[3], 'tobaadd':item[4]}
        ans.append(temp)

    cursor.close()
    conn.close()
    return ans



# 测试
if __name__ == '__main__':
    ans = get_Modify_PaperInfoFromMySql()

