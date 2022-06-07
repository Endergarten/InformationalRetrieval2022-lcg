### 附件内容

- ```main.py```：主程序（GUI）

- `my_package`

  - `__init__.py`

  - `web_spider.py`网页爬虫
  - `content_extraction.py`正文提取
  - `divide.py`分词和分句
  - `build_inverted_index.py`建立倒排索引
  - `web_rank.py`网页相关性排序

- `inverted-index`存倒排的文件

- `stop_words`结巴词典

- `word_dict`词典

- `web_source`网页源文件

- `web_text`网页正文

- `__init__.py`

- `main.py`主程序（GUI）

- `readme.md`

#### 运行环境:

Python 3.10.0

所需包：tkinter，requests， lxml，beautifulsoup4

#### 如何使用

运行`main.py`

点击`更新`按钮可以进入更新页面，在输入框中分别输入需要爬取的网页以及最大爬取数量，按下回车键或者点击确定按钮即可自动爬取网页（初始默认已经爬取苏大计科院）。

点击`搜索`按钮进入搜索页面，在输入框中输入查询语句后，按下回车键或者点击搜索按钮，结果会展示在下方的文本框中，点击文章的标题，可以自动打开对应的网页。

#### 注意事项

在更新页面如果打开网页失败，一定要重新输入网页，并成功爬取，才能够使用搜索功能，否则可能导致程序出错。
