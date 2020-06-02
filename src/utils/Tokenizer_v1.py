import os
import string


# 输入 Sting 进行分词 返回 字典 word : frequent , doclength
def Tokenizer(doc):
    Words = {}
    doclength = 0
    # 按 不可见字符 分隔成 list
    list_word_punctuation = doc.split()
    # list 去 标点 去大写      只剩重复这一冗余属性
    list_word = [word.strip(string.punctuation).lower() for word in list_word_punctuation]
    # 保存文档长度信息
    doclength = len(list_word)
    # 将 list 转换成 set 去重复性
    set_word = set(list_word)
    # :) 在循环里计算 重复数量
    for word in set_word:
        num = list_word.count(word)
        if word in Words:
            # 词已经在大字典中  更新词对应的WordInfor
            print(' 单文本不可能出现这种情况！ ')
        else:
            # 全新的词 生成对应键值对 值也是全新的
            Words[word] = num
    return Words, doclength


# 测试
if __name__ == '__main__':
    # dirpath = '../data_txt'
    # paperlist = os.listdir(dirpath)
    # print(paperlist)
    # for paper in paperlist:
    #     paperpath = os.path.join(dirpath, paper)
    #     print('-----------------------------------------------------')
    #     print(paperpath)
    #     # each paper path in loop
    #     with open(paperpath, 'r', encoding='utf-8') as f:
    #         doc = f.read()
    #         # doc = paper's string
    #         Words = Tokenizer(doc)
    #         print(Words)
    #         print(len(Words))
    Query_string = "good pig shen is good"
    query_dict, _ = Tokenizer(Query_string)
    print(query_dict)
    print(_)
