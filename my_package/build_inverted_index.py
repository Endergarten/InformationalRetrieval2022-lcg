import os
import re
import time
import math

if __name__ == '__main__':
    import divide
else:
    from . import divide


def build_inverted_index(var=None):
    print("开始建立倒排索引")
    inverted_index = dict()  # 倒排索引字典
    idft = dict()  # 每个词语的idft值
    # 首先，将字典文件读入
    # 字典文件按照不同的长度分类，相同长度的词语存在同一个列表中
    max_len = 0
    word_dict = [set() for i in range(20)]
    with open("word_dict/dict.txt.big.txt", "r", encoding="utf-8-sig") as f:
        lst = f.readlines()
    for i in range(len(lst)):
        lst[i] = lst[i].split()[0]
        word_dict[len(lst[i])].add(lst[i])
        max_len = max(max_len, len(lst[i]))

    # 然后将stopwords读入
    stopWords = set()
    for file in os.listdir("stopwords"):
        with open("stopwords/" + file, "r", encoding="utf-8-sig") as f:
            for i in f.readlines():
                stopWords.add(i[:-1])

    # 最大匹配算法
    def max_match(sentences: list):
        # 文件里的所有词语和出现次数
        file_all_words_count = dict()
        for s in sentences:
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

                        if not file_all_words_count.get(words):
                            file_all_words_count[words] = 1
                        else:
                            file_all_words_count[words] += 1
                        break

        return file_all_words_count

    def calc(file: str, file_words_count: dict):
        d = 0
        for i in file_words_count:
            file_words_count[i] = 1 + math.log10(file_words_count[i])
        for i in file_words_count:
            d += file_words_count[i] * file_words_count[i]
        d = math.sqrt(d)
        for i in file_words_count:
            if not inverted_index.get(i):
                inverted_index[i] = dict()
            inverted_index[i][int(file[:file.find('_')])] = [file_words_count[i], d]

    count = 1
    start = time.time()
    # 分文件处理
    for f in os.listdir("web_text"):
        print("正在处理第", count, "个文件")
        sentences = divide.divide_sentence(f)
        file_all_words_count = max_match(sentences)
        calc(f, file_all_words_count)
        count += 1
        if var:
            var.set(var.get() + 1)
    for i in inverted_index:
        idft[i] = math.log10((count - 1) / len(inverted_index[i]))
    print("完成！")
    end = time.time()
    print("处理用时", end - start, "秒")
    for i in os.listdir('inverted-index/'):
        os.remove('inverted-index/' + i)
    for i in inverted_index:
        with open("inverted-index/" + i + ".txt", "w", encoding="utf-8-sig") as f:
            f.write(str(idft[i]) + "\n")
            for j in inverted_index[i]:
                f.write(str(j) + " " + str(inverted_index[i][j][0]) + " " + str(inverted_index[i][j][1]) + "\n")

    print("成功建立倒排索引")
    return len(inverted_index)