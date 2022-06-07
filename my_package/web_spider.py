import requests
from queue import *
from bs4 import *
import re
import os
from tkinter import *


def web_spider(root_url='http://scst.suda.edu.cn/', max_url_nums=1000, var=None, text=None):
    for i in os.listdir('web_source'):
        os.remove('web_source/' + i)
    # max_url_nums = 1000  # 最大爬取的网页数量
    url_cnt = 0  # 当前已经爬取的网页数量
    url_set = set()  # 所有已经爬取过的网页的链接的集合
    q = Queue()  # 爬取网页的队列

    url_set.add(root_url)
    q.put(root_url)

    url_out = open('web_source/url.txt', 'w', encoding='utf-8-sig')

    while not q.empty():

        now_url = q.get()
        try:
            response = requests.get(now_url, timeout=3)
        except BaseException:
            continue
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, features='lxml')

        if 'htm' in now_url or 'html' in now_url:  # 如果是html或htm，就保存当前网页的源码
            url_cnt += 1

            print(url_cnt, now_url)
            if var:
                text.insert(END, str(url_cnt) + ' ' + now_url + '\n')
                text.yview_moveto(1)
            # 将当前网站保存下来之后命名为 编号_标题(去掉不合法字符)
            file = soup.title.text
            p = re.compile(r'''[/\\:?"<>|\s]''')
            file = re.sub(p, '', file)
            file = str(url_cnt) + '_' + file + '.txt'

            # 输出当前网页的网址和文件名
            url_out.write(file + ' ' + now_url + '\n')
            print(file)
            if var:
                text.insert(END, file + '\n')
                text.yview_moveto(1)

            with open("web_source/" + file, 'w', encoding='utf-8-sig') as fout:
                fout.write(response.text)
            if var:
                var.set(var.get() + 1)
            if url_cnt == max_url_nums:
                break
        for i in soup.find_all('a'):
            if i.attrs.get('href'):
                url = i.attrs['href']
                if 'http' not in url:  # 如果是相对url，改成绝对url
                    url = root_url[:-1] + url
                if url in url_set:
                    # 如果这个url已经处理过（在set中）或者处理的网页数量，则不处理
                    continue
                if root_url not in url:
                    # 如果url是站外链接，则不处理
                    continue
                url_set.add(url)
                q.put(url)
    return url_cnt
