#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import gtk
import sqlite3

from message import show_info
from wordpath import *


class CreateBook():
    """创建新书类
    """
    def __init__(self, builder):
        self.builder = builder

        # 单词列表文件
        self.file_choose = self.builder.get_object("filechooserbutton1")
        self.file_choose.connect("file-set", self.get_file_name)
        # 书名
        self.entry_create_name = self.builder.get_object("entry_create_name")

        self.user_choose_file = ''

        self.button_create_book = self.builder.get_object("button_create_book")
        self.button_create_book.connect("clicked", self.on_button_create_book)

    def on_button_create_book(self, widget):
        """添加按钮的回调事件
        """
        self.bookname = self.entry_create_name.get_text()

        message = ''
        if not self.user_choose_file:
            message = "请先选择单词列表文件"
        elif not self.bookname:
            message = "你必须设置书名"
        elif os.path.exists(os.path.join(USER_BOOK_PATH, self.bookname + '.book')):
            message = "此书名的文件已经存在，请换一个"

        self.bookname = os.path.join(USER_BOOK_PATH, self.bookname + '.book')
        
        is_finished = False
        if message:
            show_info(message)
        else:
            new_book = ProduceBook(self.bookname, self.builder)
            is_finished = new_book.produce_book(self.user_choose_file)

        if is_finished:
            show_info("生成新书成功！新书位于~/.wordjoy/books/目录。")
        
    def get_file_name(self, widget):
        """获得用户选择的文件名
        """
        self.user_choose_file = widget.get_filename()

class ProduceBook():
    def __init__(self, bookname, builder):
        self.builder = builder
        
        self.conn = sqlite3.connect('../books/wordjoy.book')
        self.cursor = self.conn.cursor()

        self.user_conn = sqlite3.connect(bookname)
        self.user_cursor = self.user_conn.cursor()

        self.create_table()

    def create_table(self):
        self.user_cursor.execute(
            """
            CREATE TABLE wordjoy (
            id integer PRIMARY KEY,
            name varchar(20) NOT NULL,
            status integer NOT NULL, 
            pronounce varchar(20) NOT NULL, 
            meaning varchar(200), 
            sen_en_1 varchar(100),
            sen_zh_1 varchar(200), 
            sen_en_2 varchar(100), 
            sen_zh_2 varchar(200), 
            sen_en_3 varchar(100), 
            sen_zh_3 varchar(200))
            """)

    def get_word(self, words_list):
        self.cursor.execute("""SELECT DISTINCT name, pronounce, meaning, sen_en_1, sen_zh_1, sen_en_2, sen_zh_2, sen_en_3, sen_zh_3 from wordjoy where name in %s""" % str(words_list))

        return self.cursor.fetchall()

    def produce_book(self, wordlist):
        """产生新书本
        wordlist: 用户的单词列表文件
        bookname: 生成新书的名字
        """
#         label_create_status = self.builder.get_object("label_create_status")
#         label_current_word = self.builder.get_object("label_current_word")
#         label_current_word.set_markup('<span size="x-large">正在添加单词，请耐心等待……</span>')

        words_list = []
        for word in open(wordlist):
            word = word.rstrip()
            words_list.append(word)

        words_list = tuple(words_list)
            
        result = self.get_word(words_list)

        self.user_cursor.executemany("INSERT INTO wordjoy values(NULL, ? , 0, ?, ?, ?, ?, ?, ?, ?, ?)", result)
        self.user_conn.commit()

        return True

if __name__ == '__main__':
    builder = gtk.Builder()
    builder.add_from_file(GLADE_PATH + 'createbook.xml')
    win = builder.get_object('window_createbook')

    win.connect("destroy", lambda *w: gtk.main_quit())
    CreateBook(builder)

    gtk.main()
