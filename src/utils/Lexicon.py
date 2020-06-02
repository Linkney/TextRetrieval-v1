

# 词汇的基本信息
class Lexicon:
    # 默认创建 '词汇名'  后续操作都在 updata 里
    def __init__(self, term):
        # 实例变量的数据成员
        # 词汇名
        self.term = term
        # 包含该词汇的文档数 初始化为 0
        self.docs = 0
        # {paperId : frequent}
        self.docWordInf = {}

    # 包含文档数的增量, 文档ID, 该词在该文档出现次数
    def updata(self, addDocs, paperid, num):
        # 包含该词汇的文档总数改变（增加）
        self.docs = self.docs + addDocs
        # 该词汇的 文档对应关系 增加
        if paperid in self.docWordInf:
            print("Attention ! Same PaperID in Func Update")
        else:
            # paperId 全新
            # 对该词汇增加 文档 对应关系
            self.docWordInf[paperid] = num

    def getFreqFormPaperid(self, id):
        if id in self.docWordInf:
            num = self.docWordInf[id]
        else:
            print('!No that id!')
            num = -1
        return num

    def __str__(self):
        descriptor = 'term : ' + self.term + '\n    包含该词的文档数 ： ' + str(self.docs)
        descrip_docWordInf = '\n    ' + str(self.docWordInf)
        return descriptor + descrip_docWordInf


# 测试
if __name__ == '__main__':
    print('test test 123')
    word1 = Lexicon('good')
    word1.updata(1, 2, 5)
    print(word1)
    word1.updata(1, 4, 12)
    print('--------------------------')
    print(word1)
