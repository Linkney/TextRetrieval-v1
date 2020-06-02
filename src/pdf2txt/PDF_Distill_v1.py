import warnings
warnings.filterwarnings('ignore')
import pymysql
import re
import importlib
import glob
import sys
import time
import io
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

# -----------------------------------------------------------------
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')  # 改变标准输出的默认编码
importlib.reload(sys)


# 解析 / 解析pdf文件用到的类：
# PDFParser：从一个文件中获取数据
# PDFDocument：保存获取的数据，和PDFParser是相互关联的
# PDFPageInterpreter处理页面内容
# PDFDevice将其翻译成你需要的格式
# PDFResourceManager用于存储共享资源，如字体或图像。
# ———————————————————————————————————————————————————————————————————————


# 输入一个 PDF path 返回 全面分析
def parse(PDF_path):
    # 抽取数据
    # ans 存储 由 pdf 解析得到的 string
    ans = ''
    guessTitle = ''
    guessAuthor = ''
    guessAbstract = ''

    fp = open(PDF_path, 'rb')
    # 用文件对象创建一个PDF文档分析器
    parser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器，与文档对象
    parser.set_document(doc)
    doc.set_parser(parser)
    # 提供初始化密码，如果没有密码，就创建一个空的字符串
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        print("文档不提供txt转换？遭重了！")
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDF，资源管理器，来共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释其对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 函数全局 Flag
        page_i = 1  # LTPage 编号
        titleFlag = 0  # 是否已进行 题目猜测
        authorFlag = 0  # 作者信息块猜测
        abstractFlag = 0  # 摘要信息块猜测
        # 循环遍历列表，每次处理一个LTPage内容  doc.get_pages() 获取page列表
        for page in doc.get_pages():  # 从 doc 解析出 page  从 page 解析出 layout 包含各种对象
            print("---------------------------------当前解析 LTPage [", page_i, "]")
            # 页码 阈值 1, 2 通过
            if page_i >= 3:
                break

            # 接受该页面的LTPage对象
            interpreter.process_page(page)
            # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
            layout = device.get_result()
            for x in layout:  # 遍历 Layout 中的对象
                if isinstance(x, LTTextBoxHorizontal):
                    # 当前页面 当前横向文本块 的 文字数据 result
                    results = x.get_text()

                    # 无用信息文本块过滤器
                    # 数字\n 到 v\ni\nx\nr\r\na\n    还有一些 num\nnum\nnum\n X\n
                    # 无用信息过滤  如果第一页里 只有2个长度 丢弃
                    if len(results) == 2 and page_i == 1:
                        continue
                    # 无用信息过滤 一个傻子一个回车 出现2次及以上
                    if re.match('\w\n\w\n', results, re.I) is not None:
                        continue

                    # print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    # print("当前字符串长度： ", len(results))
                    # print(results)
                    ans = ans + results  # ans 用来保存 全篇文字 用作做最后TXT文件数据

                    # 首次 有效信息 出现 猜测为题目猜测
                    if len(results) >= 20 and titleFlag == 0:
                        guessTitle = results
                        titleFlag = 1
                        continue
                    # 作者信息块猜测 ： 刚猜完题目 高度紧张   从猜完题目开始到 出现 Abstract 中间的信息
                    if titleFlag == 1 and authorFlag == 0:
                        if 'Abstract' in results:
                            # 置1 结束了 作者信息抽取
                            authorFlag = 1
                            # 该信息块 属于 摘要部分
                            guessAbstract = guessAbstract + results
                            continue
                        guessAuthor = guessAuthor + results
                    # 题目 作者 已经 关闭开关 紧接着就是 摘要 到 Introduction 为止
                    if titleFlag == 1 and authorFlag == 1 and abstractFlag == 0:
                        reresults = results.replace(' ', '')
                        if re.search('Introduction', reresults, re.I) is not None:
                            abstractFlag = 1
                            continue
                        guessAbstract = guessAbstract + results

            # Page 循环 检测 需要抽取的信息是否完成
            if authorFlag == 1 and titleFlag == 1 and abstractFlag == 1:
                break
            # 该 page 解析完毕
            page_i += 1

    return ans, guessTitle, guessAuthor, guessAbstract


# 输入一个 PDF path 返回 题目和作者信息块
def guessTitleAuthor(PDF_path):
    guessTitle = ''
    guessAuthor = ''

    fp = open(PDF_path, 'rb')
    # 用文件对象创建一个PDF文档分析器
    parser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器，与文档对象
    parser.set_document(doc)
    doc.set_parser(parser)
    # 提供初始化密码，如果没有密码，就创建一个空的字符串
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        print("文档不提供txt转换？遭重了！")
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDF，资源管理器，来共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释其对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 循环遍历列表，每次处理一个LTPage内容  doc.get_pages() 获取page列表

        page_i = 1      # LTPage 编号
        titleFlag = 0   # 是否已进行 题目猜测
        authorFlag = 0  # 作者信息块猜测
        for page in doc.get_pages():    # 从 doc 解析出 page  从 page 解析出 layout 包含各种对象
            print("--------------------------------- LTPage [", page_i, "]")

            # 如果在前两页都没能抽取到 题目和作者信息 那就可以直接废了
            if page_i == 3:
                break

            # 接受该页面的LTPage对象
            interpreter.process_page(page)

            # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
            layout = device.get_result()

            for x in layout:        # 遍历 Layout 中的对象
                if isinstance(x, LTTextBoxHorizontal):
                    results = x.get_text()  # 想要获取文本就获得对象的text属性

                    # 数字\n 到 v\ni\nx\nr\r\na\n    还有一些 num\nnum\nnum\n X\n
                    # 无用信息过滤  如果第一页里 只有2个长度 丢弃
                    if len(results) == 2 and page_i == 1:
                        # print("---------------------- Continue 跳过了2长度字符串")
                        continue
                    # 无用信息过滤 一个傻子一个回车 出现2次及以上
                    if re.match('\w\n\w\n', results, re.I) is not None:
                        continue
                    # 首次 有效信息 出现 猜测为题目猜测
                    if len(results) >= 20 and titleFlag == 0:
                        guessTitle = results
                        titleFlag = 1
                        continue
                    # 作者信息块猜测 ： 刚猜完题目 高度紧张   从猜完题目开始到 出现 Abstract 中间的信息
                    if titleFlag == 1 and authorFlag == 0:
                        if 'Abstract' in results:
                            # 置1 添加信息 直到到 Abstract
                            authorFlag = 1
                            continue
                        guessAuthor = guessAuthor + results

            if authorFlag == 1 and titleFlag == 1:
                # print("题目作者已经猜测完毕")
                break
            # 该 page  解析出来的 layout 里的 所有 TextBoxHorizontal对象完毕
            page_i += 1

    # print("Finish parse")
    return guessTitle, guessAuthor


# 输入一个 PDF path 返回 title
def guessTitle(PDF_path):
    # ans 存储 由 pdf 解析得到的 string
    ans = ''
    ''' 解析PDF文本，并保存到TXT文件中 '''
    fp = open(PDF_path, 'rb')
    # 用文件对象创建一个PDF文档分析器
    parser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器，与文档对象
    parser.set_document(doc)
    doc.set_parser(parser)

    # 提供初始化密码，如果没有密码，就创建一个空的字符串
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        print("文档不提供txt转换？遭重了！")
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDF，资源管理器，来共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释其对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 循环遍历列表，每次处理一个LTpage内容
        # doc.get_pages() 获取page列表

        for page in doc.get_pages():

            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()

            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象
            # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
            # 想要获取文本就获得对象的text属性，
            for x in layout:
                if isinstance(x, LTTextBoxHorizontal):
                    results = x.get_text()
                    # print(results)
                    # print("当前字符串长度： ", len(results))
                    if len(results) > 20:
                        print("猜测的题目是：", results)
                        guessTitle = results
                        return guessTitle
    return "no title"


# 返回大纲  多级标题
def getoutline(PDF_path):
    password = ''
    fp = open(PDF_path, 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument()
    # 连接分析器，与文档对象
    parser.set_document(doc)
    doc.set_parser(parser)

    # 提供初始化密码，如果没有密码，就创建一个空的字符串
    doc.initialize()
    outlines = doc.get_outlines()
    for (level, title, dest, action, se) in outlines:
        print("标题等级： ", level, "     标题： ", title)


# PDFDocument object represents a PDF document.
#
# Since a PDF file can be very big, normally it is not loaded at
# once. So PDF document has to cooperate with a PDF parser in order to
# dynamically import the data as processing goes.
#
# Typical usage:
#   doc = PDFDocument()
#   doc.set_parser(parser)
#   doc.initialize(password)
#   obj = doc.getobj(objid)

# 输入 PDF 文件夹路径 返回 PDF 文件夹下 所有 PDF文件具体路径的List  遍历 List 取出每篇 PDF 文件
def getPDF_pathList(PDF_dir):
    PDF_path_list = glob.glob(PDF_dir + '/*.pdf')
    return PDF_path_list


# 传入函数 测试 该函数在 PDF_dir 下所有文件下的表现
def funcPDFdirTest(func):
    PDF_path_list = getPDF_pathList('../../data_pdf')
    for i in PDF_path_list:
        print("_______________________________________________________________________________")
        print("PDF_FILE", i)
        title, author = func(i)
        print("猜测的题目： ", title)
        print("猜测的作者信息： ", author)


if __name__ == '__main__':
    # 某个具体的 PDF_path
    # PDF_path = '../../data_pdf/xxx.pdf'

    PDF_dir_path = "../../bigPDFdata"
    PDF_path_list = getPDF_pathList(PDF_dir_path)

    # 打开一个连接
    conn = pymysql.connect(host="localhost", user="root", password="root", database="paperinfo")
    # 创建一个拿数据的游标
    cursor = conn.cursor()
    ID = 0
    for localAddress in PDF_path_list:
        ID = ID + 1
        print("_______________________________________________________________________________")
        print("PDF_FILE", localAddress)
        _, title, author, abstract = parse(localAddress)
        print("猜测的题目{字符串长度：", len(title), "}： ", title)
        print("猜测的作者信息{字符串长度：", len(author), "}： ", author)
        print("猜测的摘要信息{字符串长度：", len(abstract), "}： ", abstract)

        if len(title) > 200:
            title = title[0:190] + '...'
        if len(author) > 250:
            author = author[0:250] + '...'
        if len(abstract) > 250:
            abstract = abstract[0:250] + '...'
        if len(localAddress) > 200:
            print("地址栏超长！！！")
            pass

        sql = "insert into paperinfo(title, author, abstract, localAddress) values(%s, %s, %s, %s)"
        cursor.execute(sql, (title, author, abstract, localAddress))
        # 修改值得时候 需要 commit 提交修改
        conn.commit()

    # 关闭两个玩意
    cursor.close()
    conn.close()

    print("ID:", ID)
    print('Finish')

