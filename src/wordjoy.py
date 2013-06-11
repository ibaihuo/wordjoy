#!/usr/bin/env python
#-*- coding:utf-8 -*-

import gtk
import os.path
import wordpath

from choose import ChooseBook
from sound import play
from meaningtest import Meaning
from createbook import CreateBook
from managebook import ManageBook

class WordJoy():
    """wordjoy
    """
    def __init__(self, builder):
        """
        Arguments:
        - `builder`:
        """
        self.builder = builder

        self.wordjoy_window = self.builder.get_object ("window_main")

        events_dic ={"on_sidebar_notebook_switch_page":(self.on_sidebar_notebook_switch_page, True)
                      }
        self.builder.connect_signals(events_dic)

        if not os.path.exists(wordpath.JOY_PATH):
            os.mkdir(wordpath.JOY_PATH)          # 创建~/.wordjoy
            os.mkdir(wordpath.USER_BOOK_PATH)    # 创建~/.wordjoy/books

        if not os.path.exists(wordpath.RECORD):
            record = open(wordpath.RECORD, "w")
            record.close()

        ChooseBook(self.builder)
        
        # 单词初级测试
        # Meaning(self.builder)

        notebook_recite = self.builder.get_object("notebook_recite")
        notebook_recite.set_show_tabs(False)
        notebook_recite.set_current_page(2)

        notebook_today = self.builder.get_object("notebook_today")
        notebook_today.set_show_tabs(False)
        notebook_today.set_current_page(3)


        # 请选择单词先
        notebook_test = self.builder.get_object("notebook_test")
        notebook_test.set_show_tabs(False)
        notebook_test.set_current_page(2)

        # 单词中级测试
        # Spelling(self.builder)

        # 今日任务
        # Task(self.builder)

        # 添加新书
        CreateBook(self.builder)
        notebook_manage = self.builder.get_object("notebook_manage")
        notebook_manage.set_show_tabs(False)
        notebook_manage.set_current_page(0)
        
        # 管理书本
        ManageBook(self.builder)

        # 当前进度
#         Progress(self.builder)
        notebook_progress = self.builder.get_object("notebook_progress")
#        notebook_progress.set_show_tabs(False)

    def on_sidebar_notebook_switch_page(self, widget, data, move_focus, pagenum):
        """播放菜单声音
        """
        play("menushow")


if __name__ == '__main__':
    builder = gtk.Builder()
    builder.add_from_file(wordpath.GLADE_PATH + 'wordjoy.glade')
    win_main = builder.get_object("window_main")
    win_main.connect("destroy",gtk.main_quit)

    WordJoy(builder)
    
    gtk.main()
