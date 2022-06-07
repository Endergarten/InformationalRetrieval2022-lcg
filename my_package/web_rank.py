import os
import math
import re

if __name__ == '__main__':
    import divide
else:
    from . import divide

idft = dict()  # 记录每个单词的idf值
inverted_index = dict()  # 倒排索引

allFileList = ['']  # 文件列表
url_list = ['']


def Init(var=None, url_num=0, word_num=0):
    """
    读入倒排索引和预处理的idf，倒排索引的格式为
    inverted{词语1:{文件1: [Wtd, |d1|], 文件2:[Wtd, |d2|], ……}, 词语2: {文件3:[Wtd, |d3|], ……}, ……}
    """

    global idft, inverted_index, allFileList, url_list
    idft = dict()  # 记录每个单词的idf值
    inverted_index = dict()  # 倒排索引

    allFileList = ['']  # 文件列表
    url_list = ['']

    # 读入编号对应文件的文件名和网址
    with open("web_source/url.txt", 'r', encoding='utf-8-sig') as fin:
        s = fin.readline()
        while s:
            lst = s.split()
            allFileList.append(lst[0])
            url_list.append(lst[1])
            s = fin.readline()

    # 读入倒排索引
    cnt = 0
    for file in os.listdir("inverted-index"):
        with open("inverted-index/" + file, encoding="utf-8-sig") as f:
            # 先读入第一行的idf值
            words = file[:-4]
            s = f.readline()
            idft[words] = float(s)

            # 接着依次读入含有该词语的文件编号，一次读入一行
            s = f.readline()
            while s:
                file_id, wtd, di = s.split()
                file_id = int(file_id)
                wtd = float(wtd)
                di = float(di)

                if not inverted_index.get(words):  # 如果是第一次处理这个单词
                    inverted_index[words] = {file_id: [wtd, di]}
                else:
                    inverted_index[words][file_id] = [wtd, di]

                s = f.readline()
            if var:
                cnt += 1
                var.set(int(cnt / word_num * url_num + url_num * 3))


def inter(a: list, b: list):
    # 两个有序列表取并集
    i = 0
    j = 0
    c = list()
    while i < len(a) or j < len(b):
        if i < len(a) and (j >= len(b) or a[i] < b[j]):
            c.append(a[i])
            i += 1
        elif j < len(b) and (i >= len(a) or a[i] > b[j]):
            c.append(b[j])
            j += 1
        elif i < len(a) and j < len(b) and a[i] == b[j]:
            c.append(a[i])
            i += 1
            j += 1
    return c


def show(file_list: list, words_list: list, query: str):
    """
        返回查询后的结果
        参数：file_list: list 表示含有查询词的所有文件的列表，word_list: list 是所有查询词的列表, query:str是查询语句
    """
    result = []
    # 将结果输出到以查询语句命名的文件中
    pattern = '(' + words_list[0]
    for words in words_list[1:]:
        pattern += '|' + words
    pattern += ')'
    pattern = re.compile(pattern)

    for i in file_list:

        temp = ''
        l = 20  # l表示输出词语前后l个相关片段
        with open("web_text/" + allFileList[i[0]], encoding="utf-8-sig") as fin:
            # 接着，我们打开对应的文件，去找到相关片段
            # 逐行读入
            s = fin.readline()
            while s:
                s = pattern.sub(r'#\1#', s)
                tmp = list()
                start = 0
                end = -3 * l
                for match in re.finditer(pattern, s):
                    if match.start() - l <= end:
                        end = match.end() + l
                    else:
                        if start < end:
                            tmp.append((start, end))
                        start = max(0, match.start() - l)
                        end = min(len(s) - 1, match.end() + l)
                if start < end:
                    tmp.append((start, end))
                for j in tmp:
                    # fout.write(s[i[0]:i[1]] + '\n')
                    temp += s[j[0]:j[1]].replace('\xa0', '') + '\n'
                s = fin.readline()

        title = allFileList[i[0]][:-4]

        result.append((title, temp))
    return result


def calc(file_list: list, words_list: list):
    # 计算每一个文件的余弦值，然后把列表的每一个元素从 文件编号 变为 (文件编号,cos值)
    for i in range(len(file_list)):
        cos_d_q = 0
        di_length = 0

        for words in words_list:  # 计算cos的分子部分 以及 查询 |di|
            if inverted_index.get(words) and inverted_index[words].get(file_list[i]):
                wtd = inverted_index[words][file_list[i]][0]
                cos_d_q += idft[words] * wtd
                di_length = inverted_index[words][file_list[i]][1]

        cos_d_q = cos_d_q / di_length
        file_list[i] = (file_list[i], cos_d_q)

    # 按照余弦相似度排序
    file_list.sort(key=lambda x: x[1], reverse=True)
    return file_list


def sentence_query(s: str):
    if s == "###":
        return
    if ' ' not in s:  # 如果没有分好词
        words_list = divide.max_match(s)
    else:
        words_list = s.split()
    words_list.sort(key=lambda x: len(x), reverse=True)
    # 根据词语，得到含有相关词语的所有的文件
    file_list = list()
    for words in words_list:
        if inverted_index.get(words):
            file_list = inter(file_list, sorted(inverted_index[words].keys()))

    if not file_list:
        return ""

    file_list = calc(file_list, words_list)

    return show(file_list, words_list, s)
