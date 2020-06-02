
# 获取所有的 mainInfo 表的信息 格式化后传回前端

import pymysql


# 获取所有的 PaperInfo 表的信息 格式化后传回前端
def get_Modify_MainInfoFromMySql():
    # 答卷 dk 前端还没搞好
    ans = []

    conn = pymysql.connect(host="localhost", user="root", password="root", database="paperinfo")
    cursor = conn.cursor()
    sql = "select * from maininfo"
    cursor.execute(sql)
    getFromMySql = cursor.fetchall()
    # ((ID, docCount, avdl) )
    print("数据库中的数据总量：", len(getFromMySql))
    for item in getFromMySql:
        temp = {'id': item[0], 'docCount': item[1], 'avdl': item[2]}
        ans.append(temp)

    cursor.close()
    conn.close()
    return ans


# 测试
if __name__ == '__main__':
    ans = get_Modify_MainInfoFromMySql()
    print(ans)

