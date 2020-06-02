import pickle


# 将全局变量 Words 和 Docs 进行磁盘保存
def words_Docs_dump(Words, Docs):
    with open('../../data_index/Words.pkl', 'wb') as file:
        pickle.dump(Words, file, True)
        print('Words   Dump Finish')
    with open('../../data_index/Docs.pkl', 'wb') as file:
        pickle.dump(Docs, file, True)
        print('Docs   Dump Finish')


# 从本地读取全局变量Words 和 Docs 至内存中的 global
def words_Docs_load():
    # 在不同调用的包 路径下不同  沃日 这特码 封装起来也太麻烦了 这没有框架 难顶啊 软件工程
    # 使用绝对路径来暂时解决
    with open('D:/Pycharm_code/Text_Retrieval_v1/bigindex/Words.pkl', 'rb') as file:
        Words = pickle.load(file)
        print('Words       load Finish')
    with open('D:/Pycharm_code/Text_Retrieval_v1/bigindex/Docs.pkl', 'rb') as file:
        Docs = pickle.load(file)
        print('Docs     load Finish')
    return Words, Docs
