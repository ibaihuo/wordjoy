#!/usr/bin/env python
#-*- coding:utf-8 -*-

import gtk
import random

import wordpath
from sound import play, read
from record import Record
from message import show_info, MessageDialog

# 单词测试次数
SPELLING_TIMES = 2                      # 次数至少得是2

class Spelling():
    """单词测试
    """
    def __init__(self, builder,  is_revise_mode = False):
        """
        is_revise_mode: 是否是复习模式
        """
        self.builder = builder
        self.is_revise_mode = is_revise_mode

        self.is_new_word = False        # 是一个新的单词吗？
        self.is_correct_mode = False    # 是否是改正模式？
        self.is_first_time = True       # 是否第一次测试？
        self.passed = []                # 通过的单词
        self.failed = []                # 没有通过的单词

        self.typing_sound = True
        self.sound_read_word = True
        self.sound_check_answer = True

        self.__connect_gui()            # 界面连接

        # 获得单词队列
        re = Record()

        words_list = re.get_current_record()

        self.words_len = len(words_list)

        self.queue = []
        for i in range(SPELLING_TIMES):
            temp = words_list[:]
            random.shuffle(temp)
            self.queue += temp

        self.queue_len = len(self.queue)

        self.__start_testing()

    def __start_testing(self):
        """开始测试
        """
        self.begin_next_word()

    def __connect_gui(self):
        """界面连接
        """
        # 单词输入
        self.entry_word = self.builder.get_object("entry_spell_input")
        # 显示意思
        self.label_meaning = self.builder.get_object("label_spell_meaning") 
        # 显示本单词的结果
        self.label_spell_result = self.builder.get_object("label_spell_result")
        # 显示测试进度
        self.progressbar_spell = self.builder.get_object("progressbar_spell")
        

        self.entry_word.connect("activate",self.on_enter_pressed)
        self.entry_word.connect("insert-text", self.play_type_sound)
        self.entry_word.connect("backspace", self.play_backspace_sound)

        self.button_back_mean_test = self.builder.get_object("button_back_mean_test")
        self.button_back_mean_test.connect("clicked", self.on_button_back_mean_test)

        self.button_spell_word = self.builder.get_object("checkbutton_spell_word")
        self.button_spell_sound = self.builder.get_object("checkbutton_spell_sound")
        self.button_for_answer = self.builder.get_object("checkbutton_for_answer")

        self.button_spell_word.connect("toggled", self.on_sound_control, "sound_read_word")
        self.button_spell_sound.connect("toggled", self.on_sound_control, "typing_sound")
        self.button_for_answer.connect("toggled", self.on_sound_control, "for_answer")


    def on_sound_control(self, widget, control_type):
        """声效控制
        """
        if control_type == "typing_sound":
            self.typing_sound = not self.typing_sound
        elif control_type == "for_answer":
            self.sound_check_answer = not self.sound_check_answer
        elif control_type == "sound_read_word":
            self.sound_read_word = not self.sound_read_word

    # 播放输入的声音
    def play_type_sound(self, widget, new_text, new_text_length, position, data = None):
        if not self.is_new_word and self.typing_sound:        # 不播放回车的声音
            play("type")

    def play_backspace_sound(self, widget, data = None):
        """播放退格声音或者错误提示音
        """
        if self.typing_sound:
            if not self.entry_word.get_editable():
                play ("answerno")
            else:
                play("back")

    def on_button_back_mean_test(self, widget):
        """退回到词意测试
        """
        notebook_test = self.builder.get_object("notebook_test")
        notebook_test.set_current_page(0)


    def clear_old_display_now(self):
        """消除上一个单词
        """
        if self.is_correct_mode:
            self.now = self.failed.pop()
        else:
            self.now = self.queue.pop()
        #print self.now['name']

        self.label_meaning.set_text(self.now['meaning'])
        self.label_spell_result.set_text("")

        self.entry_word.set_text("")

        if self.is_correct_mode:
            self.progressbar_spell.set_text("正在改正:剩余%d个" % len(self.failed))
            self.progressbar_spell.set_fraction(1 - float(len(self.failed))/self.how_many_faild)
        else:
            self.progressbar_spell.set_text("第%d个(共%d个)" % ((self.tested_sum + 1),  self.queue_len/2))
            self.progressbar_spell.set_fraction(float(self.tested_sum +1)/(self.queue_len/2))

        self.is_new_word = False

    def test_error_words(self):
        """测试错误的单词
        """
        if self.failed:
            self.clear_old_display_now()               # 消除上一单词，设置下一单词
        else:
            if self.is_first_time:
                self.is_correct_mode = False
                self.is_first_time = False
                self.passed = []
                self.failed = []

                show_info("加油！再复习一遍")
                self.clear_old_display_now()               # 消除上一单词，设置下一单词
            else:
                self.finish_test()

    def begin_next_word(self):
        """开始下一个单词
        """
        self.tested_sum = len(self.passed) + len(self.failed) # 测试过的单词数

        #print self.tested_sum

        # 尚未背完
        if self.tested_sum < self.queue_len/2:
            self.clear_old_display_now()  # 消除上一单词，设置下一单词
        else:
            #判断做错的题目是否为空,如果不是就进行改错
            if not self.failed:
                if self.is_first_time:
                    show_info("答完了！再复习一遍")
                    self.is_first_time = False
                    self.is_correct_mode= False
                    self.passed = []
                    self.failed = []
                    self.tested_sum = 0

                    self.begin_next_word()
                else:
                    self.finish_test()
            else:
                self.is_correct_mode = True
                show_info("现在把答错的改正一下！")

                self.how_many_faild = len(self.failed)

                self.tested_sum = 0
                self.test_error_words()

    def check_answer(self):
        """单词正确性的检查
        判断单词的正确与否，并声音提示
        """
        self.is_new_word = True
        if self.now['name'] == self.entry_word.get_text():
            if self.sound_check_answer:
                play("answerok")
            self.label_spell_result.set_text("正确!按回车继续.")
            if self.now in self.failed: # 用于改正模式
                self.failed.remove(self.now)
            self.passed.append(self.now)
        else:
            if self.sound_check_answer:
                play("answerno2")
            self.label_spell_result.set_markup("错误!正确的应该是<b>%s</b>.按回车继续" % self.now['name'])
            self.failed.append(self.now) # 在改正模式下，这个就让你非得把本单词输入正确才进行下一个

    def on_enter_pressed(self, widget, data = None):
        """按下回车时执行
        """
        if self.is_new_word:            # 第二次回车时执行
            self.entry_word.set_editable(True)
            if self.is_correct_mode:
                self.test_error_words()       # 测试错误的单词
            else:
                self.begin_next_word()
        else:                           # 第一次回车时执行
            self.check_answer()
            self.entry_word.set_editable(False)

    def finish_test(self):
        """测试完毕，保存本组单词到记录文件
        """
        # re = Record()
        # re.save_reciting_record()
        show_info("拼写测试完毕！本组词组已经写入记录，等待下次复习")

        notebook_test = self.builder.get_object("notebook_test")
        notebook_test.set_current_page(2)
        
if __name__ == "__main__":
    builder = gtk.Builder()
    builder.add_from_file(wordpath.GLADE_PATH + "spellingtest.xml")

    events_dic = {"on_window_spellingtest_destroy":gtk.main_quit}
    builder.connect_signals(events_dic)

    Spelling(builder)

    gtk.main()
