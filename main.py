from my_package import *
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar
import webbrowser
from tkinter.scrolledtext import *
import threading


class MainWindow:
    """
        主窗口
    """

    def __init__(self):
        print("正在初始化")
        # 初始化分字程序
        divide.Init()
        # 初始化好网页排序的程序
        web_rank.Init()
        # 建立并初始化主窗口
        self.window = Tk()
        self.window.title("检索系统-made by lcg")
        self.bgcolor = "#33CCFF"
        self.window.config(bg=self.bgcolor)

        # 设置窗口大小变量
        width = 1000
        height = 600
        # 窗口居中，获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
        screenwidth = self.window.winfo_screenwidth()
        screenheight = self.window.winfo_screenheight()
        size_geo = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.window.geometry(size_geo)

        # 初始化主页面和查询页面
        self.main_page = self.MainPage(self)
        self.search_page = self.SearchPage(self)
        self.updte_page = self.UpdatePage(self)
        self.back_button = Button(self.window, text="返回", font=("宋体", 15), command=self.show_main_page)

        # 打开主页面
        self.show_main_page()


        print("初始化完成")

    class MainPage:
        def __init__(self, main_window):
            """
            初始化主界面
            主界面含有两个frame
            frame1是主标题
            frame2有三个按钮，分别是更新网页，搜索，和退出
            :param window:
            """
            self.frame1 = Frame(main_window.window, bg=main_window.bgcolor)
            Label(self.frame1, text="欢迎来到LCG检索系统", font=("宋体", 30), height=5, bg=main_window.bgcolor).pack()
            self.frame2 = Frame(main_window.window, bg="#33CCFF")
            self.update_button = Button(self.frame2, text="更新", font=("宋体", 15), command=main_window.show_update_window)
            self.update_button.pack(pady=25)
            self.search_button = Button(self.frame2, text="搜索", font=("宋体", 15), command=main_window.show_search_page)
            self.search_button.pack(pady=25)
            self.quit_button = Button(self.frame2, text="退出", font=("宋体", 15),
                                      command=lambda: main_window.window.destroy())
            self.quit_button.pack(pady=25)

        def show(self):
            self.frame1.pack()
            self.frame2.pack()

        def forget(self):
            self.frame1.pack_forget()
            self.frame2.pack_forget()

    class SearchPage:

        def __init__(self, main_window):
            """
            初始化查询界面
            查询界面有两个frame
            frame1有输入框和搜索按钮
            frame2是显示结果的滚动的text
            :param window:
            """
            self.frame1 = Frame(main_window.window, bg=main_window.bgcolor)
            Label(self.frame1, text="请输入查询语句", font=("宋体", 20), bg=main_window.bgcolor).pack(pady=5)
            self.entry = Entry(self.frame1, width=70, font=("宋体", 15))
            self.entry.pack(side=LEFT, padx=50)

            # 输入框为焦点时，按下回车调用search方法
            self.entry.bind("<Return>", self.search)
            # 按下搜索按钮调用search方法
            self.search_button = Button(self.frame1, text="搜索", font=("黑体", 15), command=self.search)
            self.search_button.pack(side=RIGHT)

            self.frame2 = Frame(main_window.window)
            self.text = ScrolledText(self.frame2, width=125, height=32, bg="#DDDDDD")
            self.text.tag_config('normal', font=("宋体", 15))
            self.text.tag_config('bold', font=("宋体", 15, 'bold'))

            # 禁止用户在text中修改
            self.text.config(state='disabled')
            self.text.pack(side=LEFT, fill=BOTH)

            self.func_list = []
            self.make_func()

        def make_func(self, var=None):
            self.func_list = []
            # 创建打开指定网页的函数列表
            for i in range(len(web_rank.url_list)):
                self.func_list.append(lambda x, link=web_rank.url_list[i]: webbrowser.open(link))
                if var:
                    var.set(var.get() + 1)

        def search(self, event=None):
            self.text.config(state='normal')
            # 获取查询语句
            question = self.entry.get()
            if question:  # 如果查询内容不为空
                self.text.delete('1.0', 'end')
                # 用网页相关性排序获得结果

                # s是一个列表，其储存方式为[(文章1标题，文章1相关片段), (文章2标题，文章2相关片段), ……]
                s = web_rank.sentence_query(question)
                if s:
                    for i in s:
                        title = i[0]
                        # 获得文章的编号
                        num = int(title[:title.find('_')])
                        # 根据文章编号，获得打开该文章的网页的函数
                        func = self.func_list[num]
                        # 获得文章去掉编号之后的标题
                        title = title[title.find('_') + 1:]

                        # 用tag标签设置标题的格式和超链接（绑定函数）
                        tag = 'link>' + str(num)
                        self.text.tag_config(tag, font=("宋体", 15), foreground='blue', underline=True)
                        self.text.insert(END, title + '\n' + '\n', tag)
                        self.text.tag_bind(tag, '<Button-1>', func)

                        # 把相关片段按#分开之后，对寄奇数编号的字符需要加粗
                        temp = i[1].split('#')
                        for j in range(len(temp)):
                            if j % 2 == 0:
                                self.text.insert(END, temp[j], 'normal')
                            else:
                                self.text.insert(END, temp[j], 'bold')

                        self.text.insert(END, '\n\n')
                else:  # s 为空列表
                    messagebox.showwarning("错误", "找不到相关语句，请重新输入查询语句")
            else:  # 输入为空
                messagebox.showwarning("错误", "请输入查询语句")
            self.text.config(state='disabled')

        def show(self):
            self.frame1.pack(pady=10)
            self.frame2.pack(pady=10)

        def forget(self):
            self.frame1.pack_forget()
            self.frame2.pack_forget()

    class UpdatePage:
        def __init__(self, main_window):
            """
                更新界面
                有3个frame
                frame1是输入提示，输入框和确定按钮
                frame2是信息框，显示当前爬取的网页
                frame3是进度条
            :param main_window:
            """
            self.frame1 = Frame(main_window.window, bg=main_window.bgcolor)
            Label(self.frame1, text="请输入需要爬取的网址和爬取网页最大数量", font=("宋体", 20), bg=main_window.bgcolor).pack(pady=5)

            self.url_entry = Entry(self.frame1, width=70, font=("宋体", 15))
            self.url_entry.pack(side=LEFT, padx=40)
            # 输入框为焦点时，按下回车调用update方法
            self.url_entry.bind("<Return>", lambda x: self.update(main_window))
            self.url_entry.insert(0, "http://scst.suda.edu.cn/")
            self.num_entry = Entry(self.frame1, text="100", width=5, font=("宋体", 15))
            self.num_entry.pack(side=LEFT, padx=10)
            self.num_entry.bind("<Return>", lambda x: self.update(main_window))
            self.num_entry.insert(0, "1000")
            # 按下搜索按钮调用update方法
            self.update_button = Button(self.frame1, text="确定", font=("黑体", 15),
                                        command=lambda: self.update(main_window))
            self.update_button.pack(side=RIGHT)

            self.frame2 = Frame(main_window.window)
            self.text = ScrolledText(self.frame2, width=125, height=28, bg="#DDDDDD")
            self.text.tag_config('normal', font=("宋体", 15))
            self.text.tag_config('bold', font=("宋体", 15, 'bold'))

            # 禁止用户在text中修改
            self.text.config(state='disabled')
            # self.text.config(state='disabled')
            self.text.pack(side=LEFT, fill=BOTH)

            self.frame3 = Frame(main_window.window, bg=main_window.bgcolor)
            self.state_var = StringVar()
            self.state_var.set('')
            Label(self.frame3, textvariable=self.state_var, font=("宋体", 15), bg=main_window.bgcolor).pack()
            self.progressbar_var = IntVar()
            self.progressbar = Progressbar(self.frame3, variable=self.progressbar_var)
            self.progressbar['length'] = 850
            self.progressbar.pack()

        def func(self, main_window, url, max_url_num):
            # 爬虫、建立倒排等一系列操作
            self.update_button.config(state='disabled')
            self.num_entry.config(state='disabled')
            self.url_entry.config(state='disabled')
            main_window.back_button.config(state='disabled')
            self.progressbar_var.set(0)

            self.state_var.set("正在进行网页爬虫")
            self.text.config(state='normal')
            self.text.delete('1.0', 'end')
            url_num = web_spider(url, max_url_num, self.progressbar_var, self.text)
            if not url_num:
                messagebox.showwarning("错误", "打开网页失败，请重新输入")
                return

            self.state_var.set("正在进行正文提取")
            content_extraction(self.progressbar_var)

            self.state_var.set("正在建立倒排索引")
            word_num = build_inverted_index(self.progressbar_var, self.text)
            self.text.config(state='disabled')

            self.state_var.set("正在初始化网页排序程序")
            web_rank.Init(self.progressbar_var, url_num, word_num)

            main_window.search_page.make_func(self.progressbar_var)
            self.state_var.set("完成！")

            self.update_button.config(state='normal')
            self.num_entry.config(state='normal')
            self.url_entry.config(state='normal')
            main_window.back_button.config(state='normal')

        def update(self, main_window):

            url = self.url_entry.get()
            num = int(self.num_entry.get())
            if not url:
                messagebox.showwarning("错误", "请输入网址！")
            if not num:
                messagebox.showwarning("错误", "请输入爬取网页最大数量！")
            self.progressbar['maximum'] = num * 5
            # 开线程去做倒排，避免主窗口卡住
            threading.Thread(target=lambda: self.func(main_window, url, num)).start()

        def show(self):
            self.frame1.pack(pady=10)
            self.frame3.pack()
            self.frame2.pack(pady=10)

        def forget(self):
            self.frame1.pack_forget()
            self.frame2.pack_forget()
            self.frame3.pack_forget()

    def show_main_page(self):
        """
            打开主页面
        :return:
        """
        self.updte_page.forget()
        self.search_page.forget()
        self.back_button.pack_forget()
        self.main_page.show()

    def show_search_page(self):
        """
            打开查询页面
        :return:
        """
        self.main_page.forget()
        self.search_page.show()
        self.back_button.pack(side='bottom', pady=7)

    def show_update_window(self):
        """
            打开更新窗口
        :return:
        """
        self.main_page.forget()
        self.updte_page.show()
        self.back_button.pack(side='bottom', pady=7)


if __name__ == '__main__':
    # web_spider("http://scst.suda.edu.cn/", 1000)
    # content_extraction()
    # build_inverted_index()
    main_window = MainWindow()
    main_window.window.mainloop()
