import pickle
import math

from src.utils import Document
from src.utils.DumpLoad import words_Docs_load
from src.utils.Tokenizer_v1 import Tokenizer

# 全局数据变量 将 倒排索引 加载进内存
# 下标即 docid - 1  [Document ...]
Docs = []
# {'term' : Lexicon} ...
Words = {}


# 主程序 解析 Query 计算 每个文档 的 F(q, d) = XiYi = Xi * TF * IDF
def main(Query_string):
    # 参数表
    k = 10      # [0, +无穷)
    b = 0.5     # [0, 1]
    # 参数表 ---------------------k 控制 出现次数很多的词汇对结果的影响  b 控制 对长短文档的奖惩
    # 因为类变量出了点问题 所以暂时用硬编码
    M = 23.0  # 文章总数
    avdl = 7867.69  # 平均长度
    print('==========================================================================')
    # 对 Query 进行分词 返回 {'term' : frequent}
    query_dict, _ = Tokenizer(Query_string)
    print(query_dict)

    # 对 Query 进行  F(q, d) 计算 遍历 keyword in Query
    # -------------------------------------------------------------------------------------------------------
    # paperid : score  相关文章的相关度分数
    Score = {}
    # 遍历 Query 的词
    for keyword in query_dict:
        print('keyword : ', keyword, '\t\tfrequent : ', query_dict[keyword])
        # 如果 Query 中的词 在 Words 数据中出现过 （几乎一定是出现过）
        if keyword in Words:
            # Xi Yi 交集    Query 中的 keyword 出现在 Words 中 即 词汇库中 存在 论文中存在
            # 相当于遍历 该 词 的 链表
            for paperId in Words[keyword].docWordInf:
                # 遍历 该 词汇的 docWordInf 字典 对 该词汇存在文档 进行 算分 累加
                # BM25/Okapi  公式
                print('paperId:', paperId)
                # 该循环 keyword in Query paperid in Lexicon
                # Xi = keyword 在 query 中出现的次数
                # Yi = TF * IDF
                cwq = query_dict[keyword]
                cwd = Words[keyword].docWordInf[paperId]
                dfw = Words[keyword].docs
                ldl = Docs[paperId - 1].docLength
                # 单项 Xi * Yi
                tf = ((k + 1) * cwd / (cwd + k * (1 - b + b * (ldl / avdl))))
                idf = math.log10(((M + 1) / dfw))
                # f(q,d)
                f = cwq * tf * idf
                if paperId in Score:
                    # 已存在 分数 需要累加
                    Score[paperId] = Score[paperId] + f
                else:
                    # 第一次遇到这 paper
                    Score[paperId] = f

    # 按 分数 排序输出
    # Python 字典(Dictionary) items() 函数以列表返回可遍历的(键, 值) 元组数组。
    print('Query : ', Query_string)
    Score_list = sorted(Score.items(), key=lambda item:item[1], reverse=True)
    for item in Score_list:
        print('PaperId : ', item[0], '\t Score : ', item[1], '\t PaperName : ', Docs[item[0]-1].docName)


# 功能的封装  输入 Query 输出 AnsForQ [{'id': , 'title': , 'score':}]
def ansForQuery_V1(Query_string):
    AnsForQ = []
    words, docs = words_Docs_load()
    k = 10
    b = 0.5
    M = 23.0  # 文章总数
    avdl = 7867.69  # 平均长度
    query_dict, _ = Tokenizer(Query_string)
    Score = {}
    for keyword in query_dict:
        if keyword in words:
            for paperId in words[keyword].docWordInf:
                cwq = query_dict[keyword]
                cwd = words[keyword].docWordInf[paperId]
                dfw = words[keyword].docs
                ldl = docs[paperId - 1].docLength
                tf = ((k + 1) * cwd / (cwd + k * (1 - b + b * (ldl / avdl))))
                idf = math.log10(((M + 1) / dfw))
                f = cwq * tf * idf
                if paperId in Score:
                    Score[paperId] = Score[paperId] + f
                else:
                    Score[paperId] = f
    Score_list = sorted(Score.items(), key=lambda item: item[1], reverse=True)
    for item in Score_list:
        AnsForQ.append({'id': item[0], 'title': docs[item[0] - 1].docName, 'score': round(item[1], 2)})
    return AnsForQ


# 测试
if __name__ == '__main__':
    # 这看起来是个 if 语句 顶格的 if 语句 所以这 里不需要 global 关键词  这里和全局变量是在同地位的地方
    # 在 def 的函数里就是 局部变量了 所以需要 global 关键词 来表示 用的是 全局变量
    # 载入索引
    Words, Docs = words_Docs_load()

    Query = 'noisy model, denoisy, noisy network'
    # Query = 'convolution net model '
    # Query = 'convolution net model tricks '
    # Query = '乱搜肯定没结果 '

    # 本地测试的 print 函数
    main(Query)
    ans = ansForQuery_V1(Query)
    print(ans)
