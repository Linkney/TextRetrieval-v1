# 用于描述 文档 的数据结构
class Document:
    # 类变量
    # 平均文档长度
    avdl = -1
    # 文档总数
    docCount = -1

    def __init__(self, docName, docId, docLength):
        # 实例变量
        self.docName = docName
        self.docId = docId
        self.docLength = docLength

    # 类方法
    @classmethod
    def showDocument(self):
        descriptor = 'AVDL = ' + str(Document.avdl) + ', docCount = ' + str(Document.docCount)
        return descriptor

    def __str__(self):

        selfdoc = 'docName = ' + self.docName + ', docId = ' + str(self.docId) + ', docLength = ' \
                  + str(self.docLength)
        return selfdoc


# 测试
if __name__ == '__main__':
    doc1 = Document('end to end', 1, 100)
    doc2 = Document('pig', 2, 200)

    ll = [doc1, doc2]

    print(ll[0].avdl)
    print(ll[0].docCount)
    print(ll[1].avdl)
    print(ll[1].docCount)

    Document.avdl = 150
    Document.docCount = 2
    ll[0].avdl = 100
    # print(doc1)
    print(ll[0].showDocument())
    print(ll[0].avdl)
    print(ll[0].docCount)
    print(ll[1].avdl)
    print(ll[1].docCount)
