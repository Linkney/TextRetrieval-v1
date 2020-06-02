

# 引用树 引用节点数据结构  倒置多叉树
# 树 ：  节点  儿子
# 导致多叉树 ： 节点 父亲
class PaperNode:
    # 类变量
    # 构造函数
    def __init__(self, paperName, year, referenceNum):
        # 成员变量
        self.paperName = paperName
        self.year = year
        self.referenceNum = referenceNum
        self.URL = " to be done 本地文件地址"
        # 不知道有多少个父节点 初始化为[] 空 秃头节点
        self.father = []

    # 给当前节点加父亲
    def addFather(self, father):
        # 添加父节点  father 也是 PaperNonde类
        self.father.append(father)

    # 返回string信息
    def getinfo(self):
        ans = ''
        ans = ans + self.paperName + "    发表年份：" + str(self.year) + "    引用数：" + str(self.referenceNum)
        return ans

    # show自己和show一层父亲   这样好吧，不用去递归show了  因为这个还没有合并   show的时候展示在前端 残留 不需要
    def showTree(self):
        print(self.paperName)
        for i in range(len(self.father)):
            tempfather = self.father[i]
            print("   ", end='')
            print("-- ", tempfather.getinfo())


if __name__ == '__main__':
    print("---------------------------")
    one = PaperNode("A Latent Semantic Model with Convolutional-Pooling Structure for Information Retrieval", 2014, 409)

    two = PaperNode("Natural language processing (almost) from scratch", 2011, 5662)
    three = PaperNode("Learning to rank using gradient descent", 2005, 2277)
    four = PaperNode("Latent Dirichlet allocation", 2003, 31206)
    five = PaperNode("Parameterized concept weighting in verbose queries", 2011, 117)
    six = PaperNode("Learning deep architectures for AI In Foundamental Trends in Machine Learning", 2009, 7993)
    seven = PaperNode("A deep convolutional neural network using heterogeneous pooling for trading acoustic invariance with phonetic confusion", 2013, 159)
    eight = PaperNode("Indexing by latent semantic analysis", 1990, 15373)
    nine = PaperNode("Distributed representations of words and phrases and their compositionality", 2013, 8308)
    ten = PaperNode("A study of smoothing methods for language models applied to ad hoc information retrieval", 2001, 1845)
    one.addFather(nine)
    one.addFather(seven)
    one.addFather(two)
    one.addFather(five)
    one.addFather(six)
    one.addFather(three)
    one.addFather(four)
    one.addFather(ten)
    one.addFather(eight)
    one.showTree()