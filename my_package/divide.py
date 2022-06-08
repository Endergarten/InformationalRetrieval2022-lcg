import re
import os

word_dict = [set() for i in range(20)]  # 字典文件
max_len = 0  # 字典中的词语的最大长度
stopWords = set()


def Init():
    """
    读入倒排索引和预处理的idf，倒排索引的格式为
    inverted{词语1:{文件1: [Wtd, |d1|], 文件2:[Wtd, |d2|], ……}, 词语2: {文件3:[Wtd, |d3|], ……}, ……}

    :return:
    """
    # 首先，将字典文件读入（用于对查询语句的分词）
    # 字典文件按照不同的长度分类，相同长度的词语存在同一个列表中
    global max_len
    with open("word_dict/dict.txt.big.txt", "r", encoding="utf-8-sig") as f:
        lst = f.readlines()
    for i in range(len(lst)):
        lst[i] = lst[i].split()[0]
        word_dict[len(lst[i])].add(lst[i])
        max_len = max(max_len, len(lst[i]))

    # 然后将stopwords读入
    for file in os.listdir("stopwords"):
        with open("stopwords/" + file, "r", encoding="utf-8-sig") as f:
            for i in f.readlines():
                stopWords.add(i[:-1])


def max_match(s: str):
    """
    对查询语句分词
    :param s: 给定的语句
    :return: words_list: 词语列表
    """
    # 分词后的结果
    words_list = list()
    i = 0
    while i < len(s):
        if s[i] in ['\n', '\r', ' ', '', '\xa0', '\t', '|']:
            i += 1
            continue

        for l in range(max_len, 0, -1):  # 枚举这个词可能的长度
            if (l == 1) or (i + l <= len(s) and s[i: i + l] in word_dict[l]):  # 如果字典含有该词或者长度为1
                words = s[i: i + l]
                i += l
                if words in stopWords:  # 如果这个词语是stopwords，直接不管
                    break
                words_list.append(words)
                break
    return words_list


def divide_sentence(file: str):
    """
    分句，把整个文章按标点和换行符分开，返回句子的列表
    :param file: 文件名
    :return: 分句后的句子列表
    """
    fin = open("web_text/" + file, "r", encoding="utf-8-sig")
    temp = ''
    s = fin.readline()
    s = fin.readline()
    while s:
        temp += s
        s = fin.readline()
    sentences = re.split("[,.?:;'，。？！!；：、\n\xa0]", temp)
    fin.close()
    return sentences
