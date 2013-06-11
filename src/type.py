#!/usr/bin/env python
#-*- coding:utf-8 -*-

import gtk
import gobject
import random

import wordpath
from sound import play, read
from record import Record
from meaningtest import Meaning
from message import show_info

TYPING_TIMES = 3

class TypeWord():
    """单词跟打练习
    """
    def __init__(self, builder):
        """
        """
        self.typing_sound = True
        self.for_wrong = True
        self.read_word = True

        self.builder = builder
        self.label_follow_word = self.builder.get_object("label_follow_word")
        self.label_follow_meaning = self.builder.get_object("label_follow_meaning")
        self.label_follow_times = self.builder.get_object("label_follow_times")
        self.progressbar_follow = self.builder.get_object("progressbar_follow")

        self.entry_follow_input = self.builder.get_object("entry_follow_input")
        # self.entry_follow_input.connect("activate", self.on_enter_pressed)
        self.entry_follow_input.connect("insert-text", self.on_insert_text)
        self.entry_follow_input.connect("backspace", self.play_backspace_sound)
        self.entry_follow_input.connect("changed", self.on_entry_changed)        

        self.button_read_word = self.builder.get_object("checkbutton_read_word")
        self.button_typing_sound = self.builder.get_object("checkbutton_typing_sound")
        self.button_for_wrong = self.builder.get_object("checkbutton_for_wrong")
        
        self.button_read_word.connect("toggled", self.on_sound_control, "read_word")
        self.button_typing_sound.connect("toggled", self.on_sound_control, "typing_sound")
        self.button_for_wrong.connect("toggled", self.on_sound_control, "for_wrong")

        # 进入测试按钮按钮
        button_enter_test = self.builder.get_object("button_enter_test")
        button_enter_test.connect("clicked", self.on_button_enter_test_clicked)

        self.now_times = 1
        self.now_turn = 1

        self.start_typing()
        
    def start_typing(self):
        """开始单词拼写记忆
        """
        re = Record()
        words_list = re.get_current_record()

        self.words_len = len(words_list)
        # print words_list

        self.words_typing = []
        for i in range(TYPING_TIMES):
            temp = words_list[:]
            random.shuffle(temp)
            self.words_typing += temp

#         for item in self.words_typing:
#             print item['name']

        self.display_now_word()
            
    def on_entry_changed(self, widget):
        """输入字母后，发生
        """
        if self.character_is_wrong:
            cur_pos = widget.get_position()
            widget.delete_text(cur_pos, cur_pos+1)

        if self.character_pos == self.word_len:
            self.check_typing_progress()

    def on_insert_text(self, widget, new_text, new_text_length, position, data = None):
        """判断正误与声音提示
        """
#         print 'new_text, ', new_text
#         print self.now_word['name'], self.character_pos

        if new_text:                    # 防止清空输入框时发生事件 
            old_text = self.now_word['name'][self.character_pos]
            if new_text != old_text:
                self.character_is_wrong = True
                if self.for_wrong:
                    play("answerno")
            else:
                if self.typing_sound:
                    play("type")
                self.character_pos += 1
                self.character_is_wrong = False

    def on_sound_control(self, widget, control_type):
        """静音
        """
        if control_type == "typing_sound":
            self.typing_sound = not self.typing_sound
        elif control_type == "for_wrong":
            self.for_wrong = not self.for_wrong
        elif control_type == "read_word":
            self.read_word = not self.read_word

    def play_backspace_sound(self, widget, data = None):
        """播放退格声音或者错误提示音
        """
        if self.typing_sound:
            play("back")

        self.character_pos -= 1

    def on_enter_pressed(self, widget):
        """按下enter键，进入下一单词
        """
        pass

    def display_now_word(self):
        """显示新单词
        """
        self.now_word = self.words_typing.pop()

        if self.read_word:
            read(self.now_word['name'])

        self.character_pos = 0
        self.word_len = len(self.now_word['name'])

        self.entry_follow_input.set_text("") # 这个同样会引发insert-text事件

        self.label_follow_word.set_label(self.now_word['name'])
        self.label_follow_meaning.set_label(self.now_word['meaning'])
        self.entry_follow_input.set_max_length (self.word_len)

#        self.label_follow_times.set_label("第%d次" % self.now_times)
        self.progressbar_follow.set_text("第%d个 （共%d个）" % (self.now_turn, self.words_len))
        self.progressbar_follow.set_fraction(float(self.now_turn)/self.words_len)

    def check_typing_progress(self):
        """检查当前状态
        """
        if self.now_turn  == self.words_len:
            self.now_turn = 1
            self.now_times += 1
            if self.now_times > TYPING_TIMES:
                show_info("单词拼写记忆完毕！现在进入单词测试！")
                self.enter_testing_tab()
            else:
                show_info("第%d次拼写记忆完毕，进入第%d次拼写记忆" % ((self.now_times -1), self.now_times) )
        else:
            self.now_turn += 1

        self.display_now_word()

    def enter_testing_tab(self):
        """进入测试页面
        """
        sidebar_notebook = self.builder.get_object("sidebar_notebook")
        notebook_test = self.builder.get_object("notebook_test")

        sidebar_notebook.set_current_page(3) # 单词测试页面
        notebook_test.set_current_page(0)
        Meaning(self.builder)

    def on_button_enter_test_clicked(self, widget, data = None):
        """单击ok进入单词测试
        """
        self.enter_testing_tab()
        

if __name__ == "__main__":
    builder = gtk.Builder()
    builder.add_from_file(wordpath.GLADE_PATH + "recite.xml")

    window_recite = builder.get_object("window_recite")
    window_recite.connect('destroy', lambda *w: gtk.main_quit())

    one = TypeWord(builder)

    gtk.main()
