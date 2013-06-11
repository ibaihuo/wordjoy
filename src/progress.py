#!/usr/bin/env python
#-*- coding:utf-8 -*-

import gtk
import gobject
import os
import cPickle as pickle
from wordpath import *

(
    COLUMN_TITLE,
    COLUMN_NUM,
    COLUMN_TIMES,
    COLUMN_NEXT,
) = range(4)

COLUMN_FINISH = COLUMN_TIMES

class Progress():
    def __init__(self, builder):
        self.ing = 0
        self.finished = 0
        self.builder = builder

        label_score = self.builder.get_object("label_score")
        label_score.set_markup('<span size="xx-large">当前进度</span>')

        self.label_ing = self.builder.get_object("label_ing")
        self.label_finished = self.builder.get_object("label_finished")
        self.treeview_ing = self.builder.get_object("treeview_ing")
        self.treeview_finished = self.builder.get_object("treeview_finished")
        
        self.create_progress_list()
        self.create_finished_list()

    def create_progress_list(self, finish = None):
        """创建当前进度列表
        """
        self.treeview_ing.progress_model = gtk.ListStore(COLUMN, COLUMN, COLUMN, COLUMN)
        self.treeview_ing.set_model(self.treeview_ing.progress_model)

        self.create_progress_model()

        self.__add_title_column(self.treeview_ing, "书名",COLUMN_TITLE)
        self.__add_title_column(self.treeview_ing, "单词数",COLUMN_NUM)
        self.__add_title_column(self.treeview_ing, "剩余复习次数",COLUMN_TIMES)
        self.__add_title_column(self.treeview_ing, "下次复习时间",COLUMN_NEXT)

    def __add_title_column(self, treeview, title, column_id):
        column = gtk.TreeViewColumn(title, gtk.CellRendererText() , text = column_id)
        treeview.append_column(column)

    def create_progress_model(self):
        self.treeview_ing.progress_model.clear()
        self.ing = 0
        f = open(RECORD, "rb")
        Loading = True

        while Loading:
            try:
                record_dic = pickle.load(f)
            except pickle.UnpicklingError:
                pass
            except EOFError:
                Loading = False
            else:
                iter = self.treeview_ing.progress_model.append()
                self.ing += len(record_dic['words'])
                self.treeview_ing.progress_model.set(
                    iter,
                    COLUMN_TITLE, os.path.basename(record_dic['book']),
                    COLUMN_NUM, len(record_dic['words']),
                    COLUMN_TIMES, 7-record_dic['times'],
                    COLUMN_NEXT, record_dic['next_day'])

        self.label_ing.set_markup("你正在强化记忆<b>%d</b>个单词" % self.ing)
        f.close()

    def create_finished_list(self, finish = None):
        self.finished_model = gtk.ListStore(COLUMN, COLUMN, COLUMN, COLUMN)
        self.treeview_finished.set_model(self.finished_model)

        self.create_finished_model()

        self.__add_title_column(self.treeview_finished, "书名",COLUMN_TITLE)
        self.__add_title_column(self.treeview_finished, "单词数", COLUMN_NUM)
        self.__add_title_column(self.treeview_finished, "完成时间", COLUMN_NUM)

    def create_finished_model(self):
        self.finished_model.clear()
        self.finished = 0
        f = open(FINISHED, "rb")
        Loading = True

        while Loading:
            try:
                finished_dic = pickle.load(f)
            except pickle.UnpicklingError:
                pass
            except EOFError:
                Loading = False
            else:
                iter = self.finished_model.append()
                self.finished += len(finished_dic['words'])
                self.finished_model.set(iter,
                    COLUMN_TITLE, finished_dic['book'],
                    COLUMN_NUM, len(finished_dic['words']),
                    COLUMN_FINISH, finished_dic['next_day'])
        self.label_finished.set_markup("你已经掌握了<b>%d</b>个单词" % self.finished)
        f.close()


if __name__ == "__main__":
    glade_file = "../glade/progress_test.xml"
    builder = gtk.Builder()
    builder.add_from_file(glade_file)

    win = builder.get_object("window_progress")
    win.connect('destroy', lambda *w: gtk.main_quit())
    
    Progress(builder)

    gtk.main()
