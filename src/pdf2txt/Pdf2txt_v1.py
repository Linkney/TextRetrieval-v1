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
# 输入一个 PDF path 输出 TXT path 位置上的文件
def parse(PDF_path, TXT_path):
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

        # 循环遍历列表，每次处理一个page内容
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
                    ans = ans + results
    # windows打开文件默认是以“gbk“编码的，可能造成不识别unicode字符
    with open(TXT_path, 'a', encoding="utf-8") as f:
        num = f.write(ans)
    print('由PDF [ ', PDF_path[15:-4],' ] 解析得到的字符数为 ： ', num)


if __name__ == '__main__':
    # Python中字符串前面加上 r 表示原生字符串，数据里面的反斜杠不需要进行转义，针对的只是反斜杠
    PDF_dir_path = '../../bigPDFdata'     # bigPDFdata
    TXT_dir_path = '../../bigTXTdata'
    print('PDF_path : ', PDF_dir_path)
    print("TXT_path : ", TXT_dir_path)

    PDF_path_list = glob.glob(PDF_dir_path + '/*.pdf')
    TXT_path_list = []
    for pdf in PDF_path_list:
        # 截取 文件名   ../../data_pdf\\**********.pdf    14:-3
        temp = pdf[16:-3]
        temp = TXT_dir_path + temp + 'txt'
        TXT_path_list.append(temp)

    print("TXT_list 构造完毕，转换论文数量为 ", len(TXT_path_list))
    print(TXT_path_list)


    # -----------------------------------------------------------
    time1 = time.time()
    for i in range(len(PDF_path_list)):
        parse(PDF_path_list[i], TXT_path_list[i])
    time2 = time.time()
    # -----------------------------------------------------------
    print('总共消耗时间为 ： ', time2 - time1)
    print('Finish')

