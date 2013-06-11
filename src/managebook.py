#!/usr/bin/env python
#-*- coding:utf-8 -*-

import gtk
import os

import sqlite
import wordpath
from message import MessageDialog, show_info

(
    COLUMN_CHOOSE,
    COLUMN_WORD,
    COLUMN_MEANING,
    ) = range(3)

(
    COLUMN_DIR,
    COLUMN_PATH,
    ) = range(2)

class ListWords():
    """创建单词列表
    """
    def __init__(self, builder):
        """
        """
        self.builder = builder

        self.treeview_manage_words = self.builder.get_object("treeview_manage_words")
        self.liststore_manage_words = self.builder.get_object("liststore_manage_words")

        self.__set_header_title()

        self.button_manage_all = self.builder.get_object("button_manage_all")
        self.button_manage_all.connect("clicked", self.select_words, "All")

        self.button_manage_reverse = self.builder.get_object("button_manage_reverse")
        self.button_manage_reverse.connect("clicked", self.select_words, "Reverse")

        self.button_manage_clear = self.builder.get_object("button_manage_clear")
        self.button_manage_clear.connect("clicked", self.select_words, "Clear")


    def select_words(self, widget, how_select):
        """选择单词的方式
        """
        for i in range(self.len):
            iter = self.liststore_manage_words.get_iter(i)
            # print type(iter), iter
            is_choose = self.liststore_manage_words.get_value(iter, COLUMN_CHOOSE)
            if how_select == "All":
                update_choose = True
            elif how_select == "Reverse":
                update_choose = not is_choose
            elif how_select == "Clear":
                update_choose = False
                self.select_count = 0

            self.liststore_manage_words.set(iter, 0, update_choose)

        # 设置当前选中数目
        if how_select == "All":
            self.select_count = self.len
        elif how_select == "Reverse":
            # print self.len, self.select_count
            self.select_count = self.len - self.select_count
        elif how_select == "Shuffle":
            self.select_count = 20
        elif how_select == "Clear":
            self.select_count = 0

        self.update_select_words_count()

    def update_select_words_count(self):
        """当前选中的单词数目为多少
        """
        pass


    def __set_header_title(self):
        """设置标题行
        """
        choose = gtk.CellRendererToggle()
        choose.connect("toggled", self.__choose_toggled)
        head_title = gtk.TreeViewColumn("选择", choose, active = COLUMN_CHOOSE)
        head_title.set_sort_column_id(COLUMN_CHOOSE)
        self.treeview_manage_words.append_column(head_title)

        head_title = gtk.TreeViewColumn("单词", gtk.CellRendererText(), text = COLUMN_WORD)
        self.treeview_manage_words.append_column(head_title)

        head_title = gtk.TreeViewColumn("解释", gtk.CellRendererText(), text = COLUMN_MEANING)
        self.treeview_manage_words.append_column(head_title)

    def __choose_toggled(self, cell, path):
        """单词选择按钮
        """
        iter = self.liststore_manage_words.get_iter((int(path),)) # ??????
        choose = self.liststore_manage_words.get_value(iter, COLUMN_CHOOSE)
        if not choose:
            self.select_count += 1
        else:
            self.select_count -= 1

        self.update_select_words_count()
        choose = not choose
        self.liststore_manage_words.set(iter, COLUMN_CHOOSE, choose)
        
    def create_words_list(self, book):
        """创建单词列表
        """
        # print book
        # book = wordpath.BOOK_PATH + 'test/beginner.book'
        self.liststore_manage_words.clear()     # 清除原有数据

        db = sqlite.ConnectDB(book)
        self.words_list = db.get_words()

        self.len = len(self.words_list)

        #print words_list, len(words_list)
        for i in range(self.len):
            li_iter = self.liststore_manage_words.append()
            self.liststore_manage_words.set(li_iter,
                                    COLUMN_CHOOSE, True,
                                    COLUMN_WORD, self.words_list[i]['name'],
                                    COLUMN_MEANING, self.words_list[i]['meaning'])

        self.select_count = self.len
        self.update_select_words_count()

    def on_button_choose_ok(self, widget):
        """确定选择，设置当前选中的单词，写入内存文件
        """
        select_word_list = []
        
        for i in range(self.len):
            iter = self.liststore_manage_words.get_iter(i)
            is_choose = self.liststore_manage_words.get_value(iter, COLUMN_CHOOSE)
            if is_choose:
                word = self.liststore_manage_words.get_value(iter, COLUMN_WORD)
                select_word_list.append(word)

        # print select_word_list, len(select_word_list)

        re = Record()
        re.save_current_record(self.words_list, select_word_list)        # 保存当前记录
        
        self.change_to_recite_tab()

    def change_to_recite_tab(self):
        """功能：
        1、跳转到“单词初记”
        2、开始开始”单词初记“
        """
        self.object_list = []
        recite_tabs = self.builder.get_object("notebook_recite")
        sidebar_notebook = self.builder.get_object("sidebar_notebook")

        # 当前选中
        if self.select_count >= 5:
            #print self.dir_file
            sidebar_notebook.set_current_page(2) # 自动跳转到页面“单词初记”去
            recite_tabs.set_current_page(0) # 自动跳转到页面“单词初记”去
            self.singleton = Recite.new()       
            print "the id is:", id(self.singleton)
            self.singleton.run(self.builder) # 调用单词初记功能
        else:
            show_info("单词数少于5个，不能进行背诵！")

class TreeBooks():
    """书本列表
    """
    def __init__(self, builder, wordslist):
        """
        """
        self.builder = builder
        treeview_userbook = self.builder.get_object("treeview_userbook")
        treestore_manage_book = self.builder.get_object("treestore_manage_book")

        # 获得当前选中的条，返回gtk.TreeSelection对象
        selection = treeview_userbook.get_selection()
        # 设置选中样式
        selection.set_mode(gtk.SELECTION_SINGLE)
        # 信号/回调函数，参数为wordslist
        selection.connect("changed", self.selection_changed, wordslist)

        head_title = gtk.TreeViewColumn("选择书本", gtk.CellRendererText(), text = 0)
        treeview_userbook.append_column(head_title)

        mypiter = treestore_manage_book.append(None) # 树根：返回一个gtk.TreePiter对象
        treestore_manage_book.set(mypiter, 0, "MyBooks")
        
        if not os.listdir(wordpath.USER_BOOK_PATH):
            child_iter = treestore_manage_book.append(mypiter)
            treestore_manage_book.set(child_iter, COLUMN_DIR, "暂无书本", COLUMN_PATH, "")
        else:
            # 显示用户书本
            self.__create_book_tree(wordpath.USER_BOOK_PATH, treestore_manage_book, mypiter)

        treeview_userbook.expand_all()

    def __create_book_tree(self, dir, model, piter):
        """创建书本树
        """
        for item in os.listdir(dir):
            fullname = os.path.join(dir, item)
            if os.path.isdir(fullname):
                child_iter = model.append(piter)
                model.set(child_iter, COLUMN_DIR, item, COLUMN_PATH, fullname)
                self.__create_book_tree(fullname, model, child_iter) # 递归创建树
            else:
                item = item.split('.')[0] # 去掉文件后缀名
                child_iter = model.append(piter)
                model.set(child_iter, COLUMN_DIR, item, COLUMN_PATH, fullname)

    def selection_changed(self, widget, wordslist):
        """单击树的条目时，触发事件
        """
        (tree_model, tree_iter) = widget.get_selected()
        #print type(tree_iter)
        # 当先选择一个等级，然后点击收缩条目时，tree_iter为空。因为没有选中
        if tree_iter:
            self.dir_file = tree_model.get_value(tree_iter, COLUMN_PATH) # 单击ok时，用到self.dir_file
            # print self.dir_file
            if self.dir_file and not os.path.isdir(self.dir_file): # 等级文件
                wordslist.create_words_list(self.dir_file) # 创建单词列表

class ManageBook():
    """选择书本
    """
    def __init__(self, builder):
        """
        """
        word_list = ListWords(builder)
        TreeBooks(builder, word_list)


if __name__ == "__main__":
    builder = gtk.Builder()
    builder.add_from_file(wordpath.GLADE_PATH + "managebook.xml")

    win = builder.get_object("window_manage")
    win.connect('destroy', lambda *w: gtk.main_quit())
    ManageBook(builder)
    gtk.main()
