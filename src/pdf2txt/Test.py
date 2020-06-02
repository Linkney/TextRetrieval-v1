import re
import collections
import pymysql

result = "Abstract. As a successful a deep A deep model applied in image super-resolut" \
         "ion (SR),\nthe a Super-Resolution Convolutional Neural Network (SRCNN) [1,2] has demon-"

if 'Abstract' in result:
    print("in")



reTest1 = "6\n0\n2\ng\n"
reTest2 = "u\n3\n"
reTest3 = "1\n1\n"
reTest4 = "v\n1\n8\n9\n3\n0\n"
reTest5 = "8\n0\n6\n1\n"

# re.I 对英文大小写不敏感    \w 字母数字下划线  \n 换行符
# if re.match('\w\n\w\n', reTest3, re.I) is None:
#     print("None")


fuck = "IN TRODUC T ION"
normal = "i. Introduction"
fuck1 = fuck.replace(' ', '')


if re.search('Introduction', normal, re.I) is None:
    print("None")

print("--------------------------------------------------------------")

# 按行分隔  但是 PDF 扫描进来的数据 按的行分割时 是 PDF 内部的表面 结构 行
# 实际上应该按 句号 来分隔
lines = result.splitlines()
print(lines)
# 行内 按 空格来分隔
lines = [lines[i].split(' ') for i in range(len(lines))]
print(lines)
word = []
for line in lines:
    word.extend(line)

print(word)
# 输入为 list 对 list 中的元素 进行 相同计数
ans = collections.Counter(word)
print(ans)
print(ans.most_common(4))
print("------------------------MySQL------------------------------")

# 打开一个连接
conn = pymysql.connect(host="localhost", user="root", password="", database="paper")
# 创建一个拿数据的游标
cursor = conn.cursor()

# cursor.execute("SQL语句")    查询结果集 相当于 拿到一个列表
cursor.execute("select * from paperinfo where paperid=1")
# 拿回一个数据 result = cursor.fetchone()
# 全拿
result = cursor.fetchall()
print(result)
print(len(result))


# 关闭两个玩意
cursor.close()
conn.close()
