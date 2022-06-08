from bs4 import *
import os
from tkinter import *

def isTemp(s):
    yes = True
    for i in s:
        if i not in ['', '\n', '\r', ' ']:
            yes = False
    return yes


def content_extraction(var=None):
    for i in os.listdir('web_text'):
        os.remove('web_text/' + i)
    for f in os.listdir("web_source"):
        if f == 'url.txt':
            continue
        fOut = open("web_text/" + f, "w", encoding="utf-8-sig")
        soup = BeautifulSoup(open("web_source/" + f, encoding="utf-8-sig"), features='lxml')
        fOut.write(soup.title.text + '\n')
        s = soup.body.text
        lst = s.split('\n')
        fOut.write(lst[0][4:-3])
        for i in lst:
            if not isTemp(i):
                fOut.write(i.strip() + '\n')
        fOut.close()
        if var:
            var.set(var.get() + 1)
