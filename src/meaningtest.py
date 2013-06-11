#!/usr/bin/env python
#-*- coding:utf-8 -*-

import gtk
import random

import wordpath

from message import show_info, MessageDialog
from sound import read, play
from record import Record
from spellingtest import Spelling

class Meaning():
    """词意回想测试
    """
    def __init__(self, builder, is_revise_mode = False):
        """
        builder: 界面
        is_revise_mode: 复习模式        
        """
        self.builder = builder
        self.is_revise_mode = is_revise_mode

        self.read_word = True
        self.for_answer = True

        self.label_word = self.builder.get_object('label_meaningtest_word')

        button_mean1 = self.builder.get_object('button_mean1')
        button_mean1.connect("clicked", self.__mean_button_pressed)

        button_mean2 = self.builder.get_object('button_mean2')
        button_mean2.connect("clicked", self.__mean_button_pressed)

        button_mean3 = self.builder.get_object('button_mean3')
        button_mean3.connect("clicked", self.__mean_button_pressed)

        button_mean4 = self.builder.get_object('button_mean4')
        button_mean4.connect("clicked", self.__mean_button_pressed)

        # 再来一次
        button_once_again = self.builder.get_object('button_once_again')
        button_once_again.connect("clicked", self.__button_once_again_pressed)

        self.progressbar_meaning = self.builder.get_object('progressbar_meaning')

        self.buttons = [button_mean1, button_mean2, button_mean3, button_mean4]

#         button_continue = self.builder.get_object('button_continue')
#         button_continue.connect("button_press_event", self.__button_continue_clicked)

        button_spelling_test = self.builder.get_object('button_spelling_test')
        button_spelling_test.connect("button_press_event", self.__button_spelling_test_clicked)

        self.button_mean_word = self.builder.get_object("checkbutton_mean_word")
        self.button_mean_answer = self.builder.get_object("checkbutton_mean_answer")

        self.button_mean_word.connect("toggled", self.on_sound_control, "read_word")
        self.button_mean_answer.connect("toggled", self.on_sound_control, "for_answer")

        self.start_meaningtest()             # 开始


    def on_sound_control(self, widget, control_type):
        """声效控制
        """
        if control_type == "read_word":
            self.read_word = not self.read_word
        elif control_type == "for_answer":
            self.for_answer = not self.for_answer
            
    def __button_once_again_pressed(self, widget):
        """再背诵一次
        """
        self.start_meaningtest()

    def start_meaningtest(self):
        """初始化词意回想，采用随机采样方式，将单词丢进池子
        """
        self.queue = []                 # 单词队列
        
        re = Record()
        self.queue = re.get_current_record()

        self.queue = self.queue[:]
        random.shuffle(self.queue)

        self.word_is_passed = False     # 通过标志
        self.passed_words = []          # 通过的单词列表

        self.pool = self.queue[:]       # 池子
        random.shuffle(self.pool)
        
        self.__display_next_word()

#     def __button_continue_clicked(self, widget, event, data = None):
#         """单击继续
#         """
#         if self.word_is_passed == True:
#             self.__display_next_word()
#             self.word_is_passed = False

#         return False                    # ????

    def __enter_spelling_test(self):
        """进入拼写测试
        """
        notebook_test = self.builder.get_object("notebook_test")
        notebook_test.set_current_page(1)
        Spelling(self.builder, self.is_revise_mode)

    def __button_spelling_test_clicked(self, widget, event):
        """进入拼写测试按钮
        """
        self.__enter_spelling_test()
                
    def __withou_now_word(self):
        """除去当前单词的单词列表
        """
        without_now = self.queue[:]
        random.shuffle(without_now)
        without_now.remove(self.now)

        return without_now

    def __mean_button_pressed(self, widget, data = None):
        cn = widget.get_label()
        meaning = self.now['meaning'].replace('\n', ' ')
        if cn == meaning:
            self.passed_words.append(self.now)
            if self.for_answer:
                play("answerok")
            if len(self.passed_words) < len(self.queue):
                self.progressbar_meaning.set_text("回答正确！单击“继续”开始.")
                self.word_is_passed = True
                self.__display_next_word()
            else:
                #show_info("测试完毕.请等待下次复习！")
                dialog = MessageDialog("词意测试完毕！\n直接进入拼写测试吗?")
                response = dialog.run()
                if response == gtk.RESPONSE_YES:
                    dialog.destroy()
                    self.__enter_spelling_test()
                else:
                    dialog.destroy()
        else:
            if self.for_answer:
                play("answerno")
            self.progressbar_meaning.set_text("回答错误！请重选.")

    def __display_next_word(self):
        """显示下一单词
        """
        self.now = random.sample(self.pool, 1)[0]
        self.pool.remove(self.now)

        if self.read_word:
            read(self.now['name'])

        self.label_word.set_label(self.now['name'])
        self.progressbar_meaning.set_text("第%d个(共%d个)" % (len(self.passed_words) + 1, len(self.queue)))
        self.progressbar_meaning.set_fraction(float(len(self.passed_words)) / len(self.queue))

        answer_index = random.randint(0, 3)
        self.buttons[answer_index].set_label(self.now['meaning'].replace('\n', ' '))

        filling = random.sample(self.__withou_now_word(), 4)
        
        for button in self.buttons:
            if self.buttons.index(button) != answer_index:
                random_mean = filling[self.buttons.index(button)]
                button.set_label(random_mean['meaning'].replace('\n', ' '))

if __name__ == "__main__":
    builder = gtk.Builder()
    builder.add_from_file(wordpath.GLADE_PATH + 'meaningtest.xml')
    win = builder.get_object('window_meaning_test')

    win.connect('destroy', lambda *w: gtk.main_quit())

    Meaning(builder)

    gtk.main()
