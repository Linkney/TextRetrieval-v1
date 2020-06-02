import pickle
import math
import pymysql

from src.utils.DumpLoad import words_Docs_load
from src.utils.Tokenizer_v1 import Tokenizer

# 全局数据变量
# 下标即 docid - 1  [Document ...]
Docs = []
# {'term' : Lexicon} ...
Words = {}


# 主程序 解析 Query 计算 每个文档 的 F(q, d) = XiYi = Xi * TF * IDF
def mainSys(Query_string):
    # 返回的查询信息
    ansforquery = ""

    # 载入索引
    Words, Docs = words_Docs_load()

    conn = pymysql.connect(host="localhost", user="root", password="", database="paper")
    cursor = conn.cursor()
    sql = "select * from paperinfo"
    cursor.execute(sql)
    getfrommysql = cursor.fetchall()



    # 参数表
    k = 10
    b = 0.5
    # 参数表 ---------------------k 控制 出现次数很多的词汇对结果的影响  b 控制 对长短文档的奖惩
    print('================================================================================')
    # 对 Query 进行分词 返回 {'term' : frequent}
    query_dict, _ = Tokenizer(Query_string)
    # print(query_dict)

    # 对 Query 进行  F(q, d) 计算 遍历 keyword in Query
    # -------------------------------------------------------------------------------------------------------
    # paperid : score
    Score = {}

    for keyword in query_dict:
        # print('keyword : ', keyword, '\t\tfrequent : ', query_dict[keyword])
        if keyword in Words:
            # Xi Yi 交集    Query 中的 keyword 出现在 Words 中 即 词汇库中 存在 论文中存在
            for paperId in Words[keyword].docWordInf:
                # 遍历 该 词汇的 docWordInf 字典 对 该词汇存在文档 进行 算分 累加
                # print('paperId:', paperId)
                # 该循环 keyword in Query paperid in Lexicon
                # Xi = keyword 在 query 中出现的次数
                # Yi = TF * IDF
                cwq = query_dict[keyword]
                cwd = Words[keyword].docWordInf[paperId]
                M = 10.0
                avdl = 5890.1
                dfw = Words[keyword].docs
                ldl = Docs[paperId - 1].docLength
                # 单项 Xi * Yi
                # print(M)
                # print(avdl)
                f = cwq * ((k + 1) * cwd / (cwd + k * (1 - b + b * (ldl / avdl)))) * math.log10(((M + 1) / dfw))
                if paperId in Score:
                    # 已存在 分数 需要累加
                    Score[paperId] = Score[paperId] + f
                else:
                    # 第一次遇到这 paper
                    Score[paperId] = f

    # 按 分数 排序输出
    # Python 字典(Dictionary) items() 函数以列表返回可遍历的(键, 值) 元组数组。
    ansforquery += "--------------------------------------------------------------------------------"
    ansforquery += '\nQuery : ' + Query_string
    ansforquery += "\n--------------------------------------------------------------------------------"
    print("-------------------------------------------------------------------------------")
    print('Query : ', Query_string)
    print("-------------------------------------------------------------------------------")
    Score_list = sorted(Score.items(), key=lambda item:item[1], reverse=True)
    print(Score_list)
    for item in Score_list:
        print('PaperId : ', item[0], '\t Score : ', item[1], '\nPaperName : ', Docs[item[0]-1].docName)
        temp = getfrommysql[item[0] - 1]        # 数据行 0 id 1 title 2 author 3 abstract 4 outline
        print('\nAuthor info ： ', temp[2])
        print('Abstract info ： ', temp[3])
        print("-------------------------------------------------------------------------------")
        ansforquery += '\nPaperId : ' + str(item[0]) + '\t Score : ' + str(item[1]) + '\nPaperName : ' + Docs[item[0]-1].docName
        ansforquery += '\nAuthor info ： ' + temp[2]
        ansforquery += 'Abstract info ： ' + temp[3]
        ansforquery += "\n--------------------------------------------------------------------------------"
        break
    cursor.close()
    conn.close()

    return ansforquery


# 测试
if __name__ == '__main__':

    # Query = 'noisy model, denoisy, noisy network'
    # Query = 'convolution net model '
    Query = 'Image Denoising'

    # print(Docs[0])
    # print(Docs[0].showDocument())
    # # ??? 保存不到 类变量的值 ???

    mainSys(Query)
