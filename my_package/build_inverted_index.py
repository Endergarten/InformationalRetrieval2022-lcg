import os
import time
import math
from tkinter import *
if __name__ == '__main__':
    import divide
else:
    from . import divide


def build_inverted_index(var=None, text=None):
    print("开始建立倒排索引")
    inverted_index = dict()  # 倒排索引字典
    idft = dict()  # 每个词语的idft值

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
    sentences_cnt = 0
    for f in os.listdir("web_text"):
        print("正在处理第", count, "个文件")
        if var:
            text.insert(END, "正在处理第" + str(count) + "个文件\n")
            text.yview_moveto(1)
        # 分句
        sentences = divide.divide_sentence(f)
        sentences_cnt += len(sentences)

        # 分词并输出
        with open("web_text/" + f, 'w', encoding='utf-8') as fout:
            words_list = []
            for i in sentences:
                temp_list = divide.max_match(i)
                if not temp_list:
                    sentences_cnt -= 1
                    continue
                for words in temp_list:
                    fout.write(words + ' ')
                fout.write('\n')
                words_list.extend(temp_list)


        # 计算词语在文件中出现的次数
        file_all_words_count = dict()
        for words in words_list:
            if not file_all_words_count.get(words):
                file_all_words_count[words] = 1
            else:
                file_all_words_count[words] += 1

        calc(f, file_all_words_count)
        count += 1
        if var:
            var.set(var.get() + 1)
    for i in inverted_index:
        idft[i] = math.log10((count - 1) / len(inverted_index[i]))

    print("完成！")
    end = time.time()
    print("处理用时", end - start, "秒")
    if var:
        text.insert(END, "完成！\n处理用时" + str(end - start) +  "秒\n")
        text.yview_moveto(1)
    for i in os.listdir('inverted-index/'):
        os.remove('inverted-index/' + i)
    for i in inverted_index:
        with open("inverted-index/" + i + ".txt", "w", encoding="utf-8-sig") as f:
            f.write(str(idft[i]) + "\n")
            for j in inverted_index[i]:
                f.write(str(j) + " " + str(inverted_index[i][j][0]) + " " + str(inverted_index[i][j][1]) + "\n")

    print("成功建立倒排索引")
    print("文档数为", count - 1)
    print("句子数为", sentences_cnt)
    print("单词数为", len(inverted_index))
    if var:
        text.insert(END, "成功建立倒排索引\n文档数为" + str(count - 1) + "\n句子数为" + str(sentences_cnt) + "\n单词数为" + str(len(inverted_index)))
        text.yview_moveto(1)
    return len(inverted_index)