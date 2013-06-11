#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import gtk
import datetime
import cPickle as pickle

from wordpath import *
from record import Record
from sound import read, play
from widgets import show_info
from meaningtest import Meaning
from parse import Parse
(
    COLUMN_ID,
    COLUMN_TITLE,
    COLUMN_NUM,
    COLUMN_TIMES,
) = range(4)

class Task():
    def __init__(self, builder):
        self.builder = builder
        self.words_revise = ''
        
        self.queue = []
        self.keep = []

        # 标题标签
        self.label_task = self.builder.get_object("label_task")
        # 任务列表
        self.listview = self.builder.get_object("treeview_task")

        
        self.label_task.set_markup('<span size="xx-large">查看今日背诵任务</span>')
        button_start_task = self.builder.get_object("button_start_task")
        button_start_task.connect("clicked", self.on_start_task)

        self.create_task_list()

    def create_task_list(self):
        self.create_listview()
        notebook_today = self.builder.get_object("notebook_today")
        notebook_today.set_show_tabs(False)
        if self.queue:
            notebook_today.set_current_page(0)
        else:
            notebook_today.set_current_page(1)

    def on_start_task(self, widget, data = None):
        """切换到单词测试
        """
        if self.words_revise:
            sidebar_notebook = self.builder.get_object("sidebar_notebook")
            sidebar_notebook.set_current_page(3)
            notebook_test = self.builder.get_object("notebook_test")
            notebook_test.set_show_tabs(False)
            notebook_test.set_current_page(0)
            Meaning(self.words_revise, self.words_count, self.builder, self.record_id, is_revise_mode=True)
        else:
            show_info("请选择你要复习的内容")

    def create_listview(self):
        self.model = gtk.ListStore(COLUMN, COLUMN, COLUMN, COLUMN, COLUMN)

        self.listview.set_model(self.model)

        self.__create_model()             # 调入数据

        self.__add_title_column("ID", COLUMN_ID)
        self.__add_title_column("书名", COLUMN_TITLE)
        self.__add_title_column("单词数", COLUMN_NUM)
        self.__add_title_column("第几次复习", COLUMN_TIMES)

        selection = self.listview.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        selection.connect("changed", self.selection_changed)

    def __add_title_column(self, title, column_id):
        """增加标题
        """
        column = gtk.TreeViewColumn(title, gtk.CellRendererText(), text = column_id)
        column.set_sort_column_id(column_id)
        self.listview.append_column(column)
        
    def __create_model(self):
        """创建数据
        """
        self.model.clear()

        f = open(RECORD, "rb")
        Loading = True

        while Loading:
            try:
                record_dic = pickle.load(f)
            except pickle.UnpicklingError:
                print "截入错误，应该是空记录"
            except EOFError:
                Loading = False
                print "载入完毕"
            else:
                if datetime.date.today() >= record_dic['next_day']:
                    iter = self.model.append()
                    self.queue.append(record_dic)
                    self.model.set(iter,
                        COLUMN_ID, record_dic['id'],
                        COLUMN_TITLE, record_dic['book'],
                        COLUMN_NUM, len(record_dic['words']), 
                        COLUMN_TIMES, record_dic['times'])
        f.close()

    def selection_changed(self, widget, data = None):
        model = widget.get_selected()[0]
        iter = widget.get_selected()[1]
        if iter:
            self.words_revise = model.get_value(iter, COLUMN_TITLE)
            self.words_count = int(model.get_value(iter, COLUMN_NUM))
            self.record_id = int(model.get_value(iter, COLUMN_ID))

if __name__ == "__main__":
    builder = gtk.Builder()
    builder.add_from_file(GLADE_PATH + "today_test.xml")
    win = builder.get_object("window_task")
    win.connect('destroy', lambda *w: gtk.main_quit())
    Task(builder)
    gtk.main()
