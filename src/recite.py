#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import gtk
import random

import wordpath 
from sound import read, play
from record import Record
from type import TypeWord
(
    COLUMN_WORD,
    COLUMN_MEANING,
) = range(2)

class Recite():
    """单词初记
    """
    __inst = None
#     def __init__(self):
#         """Disabled the method
#         """
#         pass
    @staticmethod
    def new():
        """如果对象不存在，则创建一个
        """
        if not Recite.__inst:
            Recite.__inst = Recite()

        return Recite.__inst
    
    def run(self, builder):
        """运程
        """
        #print self.book
        self.builder = builder

        # 单词显示列表
        self.treeview_recite = self.builder.get_object("treeview_recite")
        self.liststore_recite = self.builder.get_object("liststore_recite")

        self.treeview_recite.set_model(self.liststore_recite)

        # 添加两标题列
        self.__add_title_column("单词", COLUMN_WORD)
        self.__add_title_column("中文解释", COLUMN_MEANING)

        # 单击时可以发音
        selection = self.treeview_recite.get_selection()
        selection.set_mode(gtk.SELECTION_BROWSE)
        selection.connect("changed", self.selection_changed)

        self.is_mute = False

        self.button_order = self.builder.get_object("button_order")
        self.button_order.connect("clicked", self.on_button_order_clicked)

        self.button_reverse = self.builder.get_object("button_reverse")
        self.button_reverse.connect("clicked", self.on_button_order_clicked, True)

        self.button_shuffle = self.builder.get_object("button_shuffle")
        self.button_shuffle.connect("clicked", self.on_button_shuffle_clicked)

        self.checkbutton_mute_recite = self.builder.get_object("checkbutton_mute_recite")
        self.checkbutton_mute_recite.connect("toggled", self.on_checkbutton_mute_recite_toggled)
        

        self.__create_words_list()

        button_enter_follow = self.builder.get_object("button_enter_follow")
        button_enter_follow.connect("clicked", self.on_button_enter_follow_clicked)

        
    def __add_title_column(self, title, column_id):
        """添加列标题
        """
        column = gtk.TreeViewColumn(title, gtk.CellRendererText(), text = column_id)
        #column.set_order_column_id(column_id)
        self.treeview_recite.append_column(column)

    def on_checkbutton_mute_recite_toggled(self, widget, data = None):
        """靜音开关
        """
        if not self.is_mute:
            self.is_mute = True
        else:
            self.is_mute = False

    def on_button_order_clicked(self, widget, is_reverse = False):
        """单词显示顺序按钮
        is_reverse: 是否逆序显示
        """
        play("buttonactive")
        
        word_new_order = []
        for i in range(self.words_len):
            iter = self.liststore_recite.get_iter(i)
            word = self.liststore_recite.get_value(iter, COLUMN_WORD)
            word_new_order.append(word)

        word_old_order = word_new_order[:]
        
        if not is_reverse:
            word_new_order.sort()
        else:
            word_new_order.sort(reverse = True)

        new_order_map = []
        for word in word_new_order:
            new_order_map.append(word_old_order.index(word))

#         print word_old_order
#         print word_new_order
#         print new_order_map

        self.liststore_recite.reorder(new_order_map)            

    def on_button_shuffle_clicked(self, widget, data = None):
        """随机乱序按钮
        """
        play("buttonactive")
        shuffle_order = range(self.words_len)

        random.shuffle(shuffle_order)
        
        self.liststore_recite.reorder(shuffle_order)
        
    def __create_words_list(self):
        """创建单词的列表
        """
        self.liststore_recite.clear()

        re_words = Record()
        self.words_list = re_words.get_current_record()

        # print self.words_list
        
        self.words_len = len(self.words_list)
        
        # print self.words_list
        for i in range(self.words_len):
            list_iter = self.liststore_recite.append()
            self.liststore_recite.set(list_iter,
                      COLUMN_WORD, self.words_list[i]['name'],
                      COLUMN_MEANING, self.words_list[i]['meaning'])
    
    def selection_changed(self, widget):
        """单击词条时触发
        1、发音
        2、显示详细的解释
        """
        meaning_detail = self.builder.get_object("textview_word_detail")
        
        select_word = ''
        # 发音
        (tree_model, tree_iter) = widget.get_selected()
        if tree_iter :
            select_word = tree_model.get_value(tree_iter, COLUMN_WORD)
            if not self.is_mute:
                read(select_word)
            
            # print select_word
            # 寻找单词的完整解释、例句
            for word in self.words_list:
                if select_word == word['name']:
                    word_dic = word

            # print word_dic

            sentence_en_3 = [(word_dic['sen_en_1'], word_dic['sen_zh_1']),
                             (word_dic['sen_en_2'], word_dic['sen_zh_2']),
                             (word_dic['sen_en_3'], word_dic['sen_zh_3'])
                             ]
            if word_dic['sen_en_1']:
                sen_display = "\n例句与用法:"
                i = 1                     # 例句标号
                for item in sentence_en_3:
                    if item[0]:
                        sen_display +=  '\n\n' + str(i) + '. ' + item[0] + '\n    ' +  item[1]
                        i += 1
            else:
                sen_display = ''

            detial = gtk.TextBuffer()
            detial.set_text(
                word_dic['name']\
                + "\n" + '[' +  word_dic['pronounce'] + ']' \
                + "\n" + word_dic['meaning']
                + "\n" \
                + sen_display)

            meaning_detail.set_buffer(detial)

            
    def on_button_enter_follow_clicked(self, widget, data = None):
        """单击OK时触发
        """
        notebook_recite = self.builder.get_object("notebook_recite")
        notebook_recite.set_current_page(1)
        TypeWord(self.builder)

if __name__ == "__main__":
    builder = gtk.Builder()
    builder.add_from_file(wordpath.GLADE_PATH + "recite.xml")

    window_recite = builder.get_object("window_recite")
    window_recite.connect('destroy', lambda *w: gtk.main_quit())

    one = Recite.new()
    one.run(builder)

    gtk.main()
