import os
import string
import pickle

from src.utils.Document import Document
from src.utils.Lexicon import Lexicon
from src.utils.Tokenizer_v1 import Tokenizer

# 全局数据变量
# 下标即 docid - 1   [Document ...]
Docs = []
# {'term' : Lexicon}
Words = {}


# 将 TXT 文件 全部转化 为 Index 并保存
#   - 构造 Docs[Document, Document ....]
#   - 构造 Words[Lexicon, Lexicon ...]
def makeIndex():
    print("Start TXT to Index...")
    global Docs
    global Words
    # TXT文件的路径
    dirpath = '../../bigTXTdata'
    # 文件路径下的遍历 papername.pdf
    paperlist = os.listdir(dirpath)
    print(paperlist)

    # docid 计数器 循环
    docid = 0
    # avdl 文档长度总和
    sumavdl = 0

    for paper in paperlist:
        paperpath = os.path.join(dirpath, paper)
        print('-----------------------------------------------------')
        docname = paper[:-4]
        print('docname:', docname)
        docid = docid + 1
        print('docid:', docid)
        with open(paperpath, 'r', encoding='utf-8') as f:
            doc_string = f.read()
            # doc = paper's string
            wordInOnePaper, doclength = Tokenizer(doc_string)
            # print(Words)
            sumavdl = sumavdl + doclength
            doc = Document(docname, docid, doclength)
            # 添加 Docs
            Docs.append(doc)
            # Docs 处理完毕， 接下来处理 Words ，相当于将一篇篇文档（小字典）灌进大字典中
            # 由 wordInOnePaper {'term' : freq} 得到 Words{'term' : class Lexicon}
            for word in wordInOnePaper:
                if word in Words:
                    # 词已经存在全局大字典中，那么更新大字典中该词对应的 Lexicon 中的信息即可
                    Words[word].updata(1, docid, wordInOnePaper[word])
                else:
                    # 全新的词 需要 新建 键值对 值 需要进行类的创建
                    lexicon = Lexicon(word)
                    lexicon.updata(1, docid, wordInOnePaper[word])
                    Words[word] = lexicon
            print('将一篇文档灌进大字典完毕')

    # 离开for循环 维护Document类变量
    Document.docCount = docid
    print("Document.docCount = ", docid)        # 23
    Document.avdl = sumavdl / Document.docCount
    print("Document.avdl = ", Document.avdl)    # 7867.695652173913

    # 展示结果
    print('=========================================================================')
    for i in range(len(Docs)):
        print(Docs[i])
    print(Document.showDocument())

    print('=========================================================================')
    print('词汇表总数 ： ', len(Words))
    print(Words[''])
    print(Words['noisy'])


# 将全局变量 Words 和 Docs 进行磁盘保存
def words_Docs_dump():
    global Words
    global Docs
    with open('../../bigindex/Words.pkl', 'wb') as file:
        pickle.dump(Words, file, True)
        print('Words   Dump Finish')
    with open('../../bigindex/Docs.pkl', 'wb') as file:
        pickle.dump(Docs, file, True)
        print('Docs   Dump Finish')


# 从本地读取全局变量Words 和 Docs 至内存中的 global
def words_Docs_load():
    global Words
    global Docs
    with open('../../bigindex/Words.pkl', 'rb') as file:
        Words = pickle.load(file)
        print('Words       load Finish')
    with open('../../bigindex/Docs.pkl', 'rb') as file:
        Docs = pickle.load(file)
        print('Docs     load Finish')


# 测试
if __name__ == '__main__':
    # 制作索引
    # makeIndex()
    # 保存索引
    # words_Docs_dump()
    # 保存的时候 保存不到 类变量 ???
    # 载入索引
    words_Docs_load()

    # print(type(Words))
    # print(len(Words))
    # print(type(Docs))
    # print(len(Docs))
    # print(Docs[0].showDocument())
    # print(type(Words['a']))
    # print(Words['net'])
    print('---------------------------------')
    # print(Document.avdl)
    # print(Document.docCount)
    print(Docs[0].avdl)
    print(Docs[0].docCount)
    print(Docs[-1].avdl)
    print(Docs[-1].docCount)

# 1、类变量为可变类型（列表、字典），通过对象修改类变量值，会同步修改类变量（后面新创建的对象也变是修改后值）
# 2、类变量为不可变类型（数字、字符串、元组），修改对象值类变量值，只会影响当前对象，不会影响类变量。
