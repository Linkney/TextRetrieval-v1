# 树的合并
# 感觉不像是树 而像是图 单向图
from src.references_Tree.PaperNode import PaperNode


def addTree(treeA, treeB):
    print("------------------------------------------------------")
    treeA.showTree()
    print("------------------------------------------------------")
    treeB.showTree()

    # 假设 treeA 为母树  treeB为子树
    checkname = treeB.paperName
    print(checkname)
    for i in range(len(treeA.father)):
        # print(treeA.father[i].paperName)
        if treeA.father[i].paperName == checkname:
            print("CHECK!!")
            # 将母树上的叶子 地址 赋值 为 以 该叶子 为树根的树
            treeA.father[i] = treeB


# 层 全局层计数器  初始论文 0 层 父亲 1 层 爷爷 2层
tower = 0

def showBigTree(tree):
    # 必须有个层 递归计数器
    global tower

    # 输出自己论文名
    print(tree.getinfo())

    for i in range(len(tree.father)):
        # 一旦进 for 父亲 层数加一
        tower += 1

        # 层前置空格
        for j in range(tower):
            print("   ", end='')

        print("-- ", end='')
        showBigTree(tree.father[i])

        # 一旦出递归 层数 减一
        tower -= 1





if __name__ == '__main__':
    print("------------------------------------------------------")
    Tree_one = PaperNode("A Latent Semantic Model with Convolutional-Pooling Structure for Information Retrieval", 2014, 409)

    two = PaperNode("Natural language processing (almost) from scratch", 2011, 5662)
    three = PaperNode("Learning to rank using gradient descent", 2005, 2277)
    four = PaperNode("Latent Dirichlet allocation", 2003, 31206)
    five = PaperNode("Parameterized concept weighting in verbose queries", 2011, 117)
    six = PaperNode("Learning deep architectures for AI In Foundamental Trends in Machine Learning", 2009, 7993)
    seven = PaperNode("A deep convolutional neural network using heterogeneous pooling for trading acoustic invariance with phonetic confusion", 2013, 159)
    eight = PaperNode("Indexing by latent semantic analysis", 1990, 15373)
    nine = PaperNode("Distributed representations of words and phrases and their compositionality", 2013, 8308)
    ten = PaperNode("A study of smoothing methods for language models applied to ad hoc information retrieval", 2001, 1845)
    Tree_one.addFather(nine)
    Tree_one.addFather(seven)
    Tree_one.addFather(two)
    Tree_one.addFather(five)
    Tree_one.addFather(six)
    Tree_one.addFather(three)
    Tree_one.addFather(four)
    Tree_one.addFather(ten)
    Tree_one.addFather(eight)
    # Tree_one.showTree()

    print("------------------------------------------------------")
    # Tree_one 的 four 叶子
    Tree_two = PaperNode("Latent Dirichlet allocation", 2003, 31206)
    two_one = PaperNode("Using Maximum Entropy for Text Classification", 1999, 1138)
    two_two = PaperNode("Statistical methods for speech recognition", 1997, 2892)
    Tree_two.addFather(two_one)
    Tree_two.addFather(two_two)
    # Tree_two.showTree()

    addTree(Tree_one, Tree_two)

    print("TEST ADD TREE A & B ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    print(Tree_one.father[6].father)
    print(Tree_one.father[7].father)

    print("Show Big tree ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    showBigTree(Tree_one)